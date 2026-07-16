from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Test Platformer
        page.goto("http://localhost:8000/platformer.html")
        page.wait_for_timeout(3000)
        page.screenshot(path="/home/jules/platformer_screenshot.png")
        print("Platformer loaded successfully.")

        # Test Shooter
        page.goto("http://localhost:8000/shooter.html")
        page.wait_for_timeout(2000)
        page.screenshot(path="/home/jules/shooter_screenshot.png")
        print("Shooter loaded successfully.")

        browser.close()

if __name__ == "__main__":
    run()
