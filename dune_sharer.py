import os
import time
from playwright.sync_api import sync_playwright, TimeoutError
from PIL import Image
import tweepy
from dotenv import load_dotenv
import logging
from datetime import datetime

class DuneSharer:
    """Dune Analytics Dashboard Sharer"""
    
    def __init__(self, screenshots_dir=None):
        """Initialize DuneSharer"""
        self.logger = logging.getLogger(__name__)
        
        # Set directories
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.logs_dir = os.path.join(self.output_dir, 'logs')
        self.screenshots_dir = screenshots_dir or os.path.join(self.base_dir, 'screenshots')
        
        # Create necessary directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        # Configure logging
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(os.path.join(self.logs_dir, 'app.log'))
            ]
        )

    def check_browser_connection(self):
        """Check if browser is running in remote debugging mode"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
                browser.close()
                return True
        except Exception as e:
            self.logger.error("Could not connect to browser. Please start Chrome with remote debugging:")
            self.logger.error("/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
            return False

    def normalize_browser_view(self, page):
        """Normalize browser view settings"""
        # Set browser zoom to 100%
        page.evaluate("""() => {
            document.body.style.zoom = '100%';
            document.body.style.transform = 'scale(1)';
            document.body.style.transformOrigin = '0 0';
        }""")
        
        # Get device pixel ratio
        device_pixel_ratio = page.evaluate("window.devicePixelRatio")
        self.logger.info(f"Device pixel ratio: {device_pixel_ratio}")
        
        # Set viewport size to standard dimensions
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        return device_pixel_ratio

    def get_element_metrics(self, element):
        """Get detailed metrics for an element"""
        return element.evaluate("""el => {
            const rect = el.getBoundingClientRect();
            const computed = window.getComputedStyle(el);
            const parent = el.parentElement ? el.parentElement.getBoundingClientRect() : null;
            
            return {
                // Element metrics
                rect: {
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height,
                    top: rect.top,
                    right: rect.right,
                    bottom: rect.bottom,
                    left: rect.left
                },
                // Position relative to parent
                relativeToParent: parent ? {
                    x: rect.x - parent.x,
                    y: rect.y - parent.y,
                    top: rect.top - parent.top,
                    left: rect.left - parent.left
                } : null,
                // Computed styles
                computed: {
                    position: computed.position,
                    display: computed.display,
                    transform: computed.transform,
                    scale: computed.scale,
                    zoom: computed.zoom
                },
                // Viewport information
                viewport: {
                    scrollX: window.pageXOffset,
                    scrollY: window.pageYOffset,
                    visualViewportWidth: window.visualViewport ? window.visualViewport.width : window.innerWidth,
                    visualViewportHeight: window.visualViewport ? window.visualViewport.height : window.innerHeight,
                    visualViewportScale: window.visualViewport ? window.visualViewport.scale : 1
                }
            };
        }""")

    def capture_chart_element(self, page, element, screenshot_path, device_pixel_ratio=1):
        """Capture a chart element professionally"""
        try:
            # Get detailed element metrics
            metrics = self.get_element_metrics(element)
            self.logger.debug(f"Element metrics: {metrics}")
            
            # Calculate actual physical pixel dimensions
            physical_width = metrics['rect']['width'] * device_pixel_ratio
            physical_height = metrics['rect']['height'] * device_pixel_ratio
            
            # Ensure element is in viewport and wait for stability
            element.evaluate("""(el, metrics) => {
                const rect = el.getBoundingClientRect();
                const viewportHeight = metrics.viewport.visualViewportHeight;
                const viewportWidth = metrics.viewport.visualViewportWidth;
                
                // If element is not in viewport, scroll to appropriate position
                if (rect.top < 0 || rect.bottom > viewportHeight) {
                    const centerY = rect.top + rect.height / 2;
                    const scrollY = centerY - viewportHeight / 2;
                    window.scrollTo({
                        top: window.pageYOffset + scrollY,
                        behavior: 'instant'
                    });
                }
            }""", metrics)
            
            # Wait for scroll and repaint
            time.sleep(1)
            
            # Get element position and size
            box = element.bounding_box()
            if not box:
                self.logger.error("Failed to get element bounding box")
                return False
            
            try:
                # Take screenshot using device scale
                element.screenshot(
                    path=screenshot_path,
                    scale="device"
                )
                
                # Verify screenshot dimensions
                with Image.open(screenshot_path) as img:
                    actual_width, actual_height = img.size
                    self.logger.info(f"Screenshot dimensions: {actual_width}x{actual_height} " +
                                   f"(expected: {physical_width:.0f}x{physical_height:.0f})")
                    
                    # Resize image if dimensions don't match
                    if abs(actual_width - physical_width) > 5 or abs(actual_height - physical_height) > 5:
                        self.logger.info("Resizing image to match physical dimensions")
                        resized_img = img.resize(
                            (int(physical_width), int(physical_height)),
                            Image.Resampling.LANCZOS
                        )
                        resized_img.save(screenshot_path, quality=95, optimize=True)
                    
                return True
                
            except Exception as e:
                self.logger.error(f"Error taking screenshot: {str(e)}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error capturing chart element: {str(e)}")
            return False

    def download_dune_dashboard(self, url):
        """Download charts from a Dune Analytics dashboard"""
        # First check browser connection
        if not self.check_browser_connection():
            raise Exception("Please start Chrome in remote debugging mode first")
            
        try:
            playwright = sync_playwright().start()
            try:
                # Connect to existing browser instance
                browser = playwright.chromium.connect_over_cdp('http://127.0.0.1:9222')
                default_context = browser.contexts[0]
                pages = default_context.pages
                
                target_page = None
                for page in pages:
                    if url in page.url:
                        target_page = page
                        self.logger.info("Found existing dashboard page")
                        break
                
                if not target_page:
                    # If no existing page found, open in current context
                    target_page = default_context.new_page()
                    target_page.goto(url)
                    target_page.wait_for_load_state("networkidle", timeout=60000)
                    self.logger.info("Opened dashboard in new page")
                
                # Normalize browser view settings
                device_pixel_ratio = self.normalize_browser_view(target_page)
                
                # Wait for page load and render
                target_page.bring_to_front()
                target_page.wait_for_load_state("networkidle", timeout=60000)
                time.sleep(5)
                
                # Find chart containers
                container_selector = "article.react-grid-item"
                target_page.wait_for_selector(container_selector, state="visible", timeout=30000)
                containers = target_page.query_selector_all(container_selector)
                
                if not containers:
                    raise Exception("No chart containers found on the dashboard")
                
                self.logger.info(f"Found {len(containers)} potential containers")
                
                # Process each container
                screenshots = []
                for i, container in enumerate(containers):
                    try:
                        # Wait for container stability
                        container.wait_for_element_state("stable", timeout=5000)
                        
                        # Get container metrics
                        metrics = self.get_element_metrics(container)
                        self.logger.debug(f"Container {i} metrics: {metrics}")
                        
                        # Check container size, skip if too small
                        if metrics['rect']['width'] < 300 or metrics['rect']['height'] < 200:
                            self.logger.debug(f"Skipping container {i} due to small size")
                            continue
                        
                        # Check if it's a list container
                        is_list = False
                        list_element = container.query_selector("table, .ag-root, [role='grid'], .ReactVirtualized__Grid")
                        if list_element:
                            is_list = True
                            self.logger.info(f"Found list element in container {i}")
                        
                        # Check for chart elements
                        if not is_list:
                            # 1. Check for canvas element (usually charts)
                            chart_element = container.query_selector("canvas")
                            if not chart_element:
                                # 2. Check for specific chart-related class names
                                chart_element = container.query_selector(".echarts-for-react, .highcharts-container, [data-testid='chart']")
                            if not chart_element:
                                # 3. Check for large SVGs (usually charts)
                                svg_elements = container.query_selector_all("svg")
                                for svg in svg_elements:
                                    svg_box = svg.bounding_box()
                                    if svg_box and svg_box['width'] > 200 and svg_box['height'] > 150:
                                        chart_element = svg
                                        break
                            
                            if not chart_element:
                                self.logger.debug(f"No chart element found in container {i}")
                                continue
                        
                        # Create screenshot path
                        screenshot_path = os.path.join(self.screenshots_dir, f'content_{i}.png')
                        
                        # Capture content
                        if self.capture_chart_element(target_page, container, screenshot_path, device_pixel_ratio):
                            self.logger.info(f"Successfully captured {'list' if is_list else 'chart'} {i}")
                            screenshots.append({
                                'index': i,
                                'type': 'list' if is_list else 'chart',
                                'screenshot': screenshot_path
                            })
                        else:
                            self.logger.warning(f"Failed to capture {'list' if is_list else 'chart'} {i}")
                    except Exception as e:
                        self.logger.error(f"Error processing container {i}: {str(e)}")
                        continue
                
                self.logger.info(f"Successfully captured {len(screenshots)} items")
                
                return screenshots
                
            finally:
                playwright.stop()
        except Exception as e:
            self.logger.error(f"Error capturing dashboard: {str(e)}")
            raise

    def process_dashboard(self, dashboard_url):
        """Main function to process a dashboard and create a thread"""
        try:
            screenshots = self.download_dune_dashboard(dashboard_url)
            if screenshots:
                return "Screenshots captured successfully!"
            else:
                return "Error: No charts found in the dashboard"
        except Exception as e:
            self.logger.error(f"Error processing dashboard: {str(e)}")
            raise

    def share_on_twitter(self, dashboard_url, screenshots):
        """Share screenshots on Twitter"""
        try:
            # Connect to user's Chrome browser via CDP
            playwright = sync_playwright().start()
            try:
                # Connect to user's Chrome browser
                browser = playwright.chromium.connect_over_cdp('http://127.0.0.1:9222')
                default_context = browser.contexts[0]
                
                # Get all pages
                pages = default_context.pages
                
                # Check if Twitter is already open
                twitter_page = None
                for page in pages:
                    if 'twitter.com' in page.url:
                        twitter_page = page
                        self.logger.info("Found existing Twitter page")
                        break
                
                if not twitter_page:
                    # If Twitter is not open, create new tab
                    twitter_page = default_context.new_page()
                    twitter_page.goto('https://twitter.com/compose/tweet')
                else:
                    # If Twitter is open, navigate to compose page
                    twitter_page.bring_to_front()
                    twitter_page.goto('https://twitter.com/compose/tweet')
                
                # Wait for tweet button
                twitter_page.wait_for_selector('div[data-testid="tweetTextarea_0"]')
                
                # Enter tweet text
                tweet_text = f"Check out this Dune Analytics dashboard: "
                twitter_page.fill('div[data-testid="tweetTextarea_0"]', tweet_text)
                
                # Upload screenshots
                for screenshot in screenshots:
                    file_input = twitter_page.wait_for_selector('input[type="file"]')
                    file_input.set_input_files(screenshot['screenshot'])
                    time.sleep(1)  # Wait for upload
                
                # Click tweet button
                twitter_page.click('div[data-testid="tweetButton"]')
                
                # Wait for tweet to complete
                time.sleep(3)
                
                self.logger.info("Successfully shared on Twitter")
                
            finally:
                # Don't close browser as it's user's browser
                playwright.stop()
                
        except Exception as e:
            self.logger.error(f"Error sharing on Twitter: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    dashboard_url = input("Please enter the Dune dashboard URL: ")
    sharer = DuneSharer()
    result = sharer.process_dashboard(dashboard_url)
    print(result)
