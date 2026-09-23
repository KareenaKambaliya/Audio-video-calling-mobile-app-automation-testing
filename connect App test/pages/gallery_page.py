"""
Gallery & Media Viewer Page Object for Plutomen Connect.
Represents GalleryDetailActivity and ChatImageViewerActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class GalleryPage(BasePage):
    """Page Object for Gallery Media Browser, Full-Screen Viewer, and Download."""

    GALLERY_ITEM = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@class, 'ImageView') or "
        "contains(@resource-id, 'img_thumbnail')]"
    )

    FULL_SCREEN_IMAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'activity_image_viewer') or contains(@class, 'PhotoView') or "
        "contains(@resource-id, 'img_full_screen') or contains(@class, 'ImageView')]"
    )

    BTN_DOWNLOAD = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'download') or contains(@resource-id, 'txtSaveMedia') or "
        "contains(@resource-id, 'iv_download') or contains(@content-desc, 'Download')]"
    )

    BTN_DELETE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'delete') or contains(@resource-id, 'iv_delete') or "
        "contains(@content-desc, 'Delete')]"
    )

    CONFIRM_DELETE_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Delete') or contains(@text, 'Yes') or contains(@resource-id, 'button1')]"
    )

    ERROR_IMAGE_VIEW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Failed to load') or contains(@resource-id, 'error') or "
        "contains(@resource-id, 'broken')]"
    )

    def open_first_media_item(self):
        """Open the first media item in gallery."""
        logger.info("Opening media item from gallery...")
        self.click(self.GALLERY_ITEM, timeout=5)

    def is_full_screen_viewer_displayed(self) -> bool:
        """Verify full-screen media viewer is open."""
        return (
            "imageviewer" in self.get_current_activity().lower()
            or "gallerydetail" in self.get_current_activity().lower()
            or self.is_displayed(self.FULL_SCREEN_IMAGE, timeout=5)
        )

    def swipe_next_media(self):
        """Perform horizontal swipe to next media item."""
        logger.info("Swiping to next media item...")
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.8)
        end_x = int(size['width'] * 0.2)
        y = size['height'] // 2
        self.driver.swipe(start_x, y, end_x, y, 300)

    def download_media(self):
        """Download media to local storage."""
        logger.info("Downloading media item...")
        if self.is_displayed(self.BTN_DOWNLOAD, timeout=4):
            self.click(self.BTN_DOWNLOAD)

    def delete_media(self):
        """Delete media item."""
        logger.info("Deleting media item...")
        if self.is_displayed(self.BTN_DELETE, timeout=4):
            self.click(self.BTN_DELETE)
            if self.is_displayed(self.CONFIRM_DELETE_BUTTON, timeout=3):
                self.click(self.CONFIRM_DELETE_BUTTON)
