# perception/camera.py — Image capture and obstacle detection

import cv2
import numpy as np
import logging

log = logging.getLogger(__name__)

# Obstacle detection tuning constants
OBSTACLE_ROI_TOP      = 0.5    # Only look at the bottom 50% of the frame (what's directly ahead)
OBSTACLE_MIN_AREA     = 8000   # Minimum contour area (px²) to count as an obstacle
OBSTACLE_EDGE_LOW     = 50     # Canny edge detection lower threshold
OBSTACLE_EDGE_HIGH    = 150    # Canny edge detection upper threshold
OBSTACLE_BLUR_KERNEL  = (5, 5) # Gaussian blur before edge detection (reduces noise)


class Camera:

    def __init__(
        self,
        device_index: int = 0,
        width: int        = 640,
        height: int       = 480
    ):
        """
        Opens the camera and configures resolution.
        Fails gracefully if no camera is found — Guido boots without it.
        """
        self.device_index = device_index
        self.width        = width
        self.height       = height
        self._cap         = None

        self._connect()

    # ----------------------------
    # Public API
    # ----------------------------

    def capture_frame(self) -> np.ndarray | None:
        """
        Grabs a single frame from the camera.
        Returns the frame as a NumPy BGR array, or None if unavailable.
        """
        if not self.is_connected():
            log.warning("Camera not connected — cannot capture frame.")
            return None

        ret, frame = self._cap.read()

        if not ret or frame is None:
            log.warning("Camera returned empty frame.")
            return None

        return frame

    def is_path_clear(self) -> bool:
        """
        Main method for navigation safety checks.
        Returns True if no significant obstacle is detected ahead.
        Returns True (safe) if camera is unavailable — don't block movement
        just because the camera is missing.
        """
        frame = self.capture_frame()

        if frame is None:
            log.warning("No frame available — assuming path is clear.")
            return True

        obstacle_detected = self._detect_obstacle(frame)

        if obstacle_detected:
            log.warning("⚠ Obstacle detected ahead!")
        else:
            log.debug("Path is clear.")

        return not obstacle_detected

    def is_connected(self) -> bool:
        """Returns True if the camera is open and responding."""
        return self._cap is not None and self._cap.isOpened()

    def release(self):
        """Cleanly releases the camera resource."""
        if self.is_connected():
            self._cap.release()
            log.info("Camera released.")
        self._cap = None

    # ----------------------------
    # Obstacle detection
    # ----------------------------

    def _detect_obstacle(self, frame: np.ndarray) -> bool:
        """
        Analyses a frame for obstacles using edge detection + contour analysis.

        Pipeline:
          1. Crop to the bottom half of the frame (robot's eye level = close proximity)
          2. Convert to grayscale
          3. Gaussian blur to reduce noise/texture false positives
          4. Canny edge detection to find object boundaries
          5. Find contours — large contours mean something solid is close
          6. If any contour exceeds OBSTACLE_MIN_AREA → obstacle
        """
        roi = self._get_roi(frame)

        gray    = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, OBSTACLE_BLUR_KERNEL, 0)
        edges   = cv2.Canny(blurred, OBSTACLE_EDGE_LOW, OBSTACLE_EDGE_HIGH)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= OBSTACLE_MIN_AREA:
                log.debug(f"Obstacle contour area: {area:.0f}px²")
                return True

        return False

    def _get_roi(self, frame: np.ndarray) -> np.ndarray:
        """
        Crops the frame to the Region Of Interest (ROI) —
        the bottom portion of the image where close obstacles appear.

        OBSTACLE_ROI_TOP = 0.5 means: take everything below the vertical midpoint.
        Lower this value to look further ahead; raise it to focus closer.
        """
        h = frame.shape[0]
        top = int(h * OBSTACLE_ROI_TOP)
        return frame[top:h, :]

    # ----------------------------
    # Debug / Dev utilities
    # ----------------------------

    def show_debug_view(self):
        """
        Opens a live window showing the camera feed + edge detection overlay.
        Press 'q' to close.
        Useful during development to tune OBSTACLE_MIN_AREA and thresholds.
        Only call this manually — never in the main loop.
        """
        if not self.is_connected():
            log.error("Camera not connected — cannot show debug view.")
            return

        log.info("Debug view open — press 'q' to quit.")

        while True:
            frame = self.capture_frame()
            if frame is None:
                break

            roi     = self._get_roi(frame)
            gray    = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, OBSTACLE_BLUR_KERNEL, 0)
            edges   = cv2.Canny(blurred, OBSTACLE_EDGE_LOW, OBSTACLE_EDGE_HIGH)

            # Draw contours on the ROI for visual feedback
            contours, _ = cv2.findContours(
                edges,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            roi_vis = roi.copy()
            for contour in contours:
                area = cv2.contourArea(contour)
                color = (0, 0, 255) if area >= OBSTACLE_MIN_AREA else (0, 255, 0)
                cv2.drawContours(roi_vis, [contour], -1, color, 2)

            # Stack original ROI and edge view side by side
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            combined  = np.hstack([roi_vis, edges_bgr])

            cv2.imshow("Guido Camera Debug | left: contours | right: edges", combined)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cv2.destroyAllWindows()

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _connect(self):
        """
        Tries to open the camera at the given device index.
        Sets resolution if the camera supports it.
        Fails gracefully if no camera is available.
        """
        try:
            cap = cv2.VideoCapture(self.device_index)

            if not cap.isOpened():
                raise OSError(f"Could not open camera at index {self.device_index}")

            cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            self._cap = cap
            actual_w  = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_h  = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            log.info(f"Camera [{self.device_index}] opened at {actual_w}x{actual_h}.")

        except Exception as e:
            log.error(f"Failed to open camera [{self.device_index}]: {e}")
            log.warning("Guido will run without camera — obstacle detection disabled.")
            self._cap = None
