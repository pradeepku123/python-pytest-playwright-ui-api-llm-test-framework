
import pytest
import asyncio
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_debug_portfolio_button(page):
    # Login
    await page.goto("http://localhost:4200/login")
    await page.fill("#username", "admin")
    await page.fill("#password", "superadmin")
    await page.click("button:has-text('Sign In')")
    await page.wait_for_url("**/dashboard")
    
    # Go to Portfolio
    await page.goto("http://localhost:4200/portfolio")
    await page.wait_for_load_state("networkidle")
    
    # Analyze Button
    print("\n--- BUTTON ANALYSIS ---")
    btn_handle = await page.evaluate_handle("""() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        return buttons.find(b => b.textContent.includes('Add Investment'));
    }""")
    
    if btn_handle:
        print("Button Found!")
        is_visible = await btn_handle.is_visible()
        print(f"Is Visible: {is_visible}")
        outer_html = await btn_handle.evaluate("el => el.outerHTML")
        print(f"HTML: {outer_html}")
        
        # Click
        print("Clicking button via JS...")
        await btn_handle.click()
    else:
        print("Button NOT Found using text 'Add Investment'")
        
    await page.wait_for_timeout(2000)
    
    # Analyze Modal
    print("\n--- MODAL ANALYSIS ---")
    modal_content = await page.evaluate("""() => {
        const modal = document.querySelector('.modal-content') || document.querySelector('.modal-body') || document.querySelector('div[role="dialog"]');
        return modal ? modal.outerHTML : 'Modal NOT Found';
    }""")
    print(f"Modal Content/Body: {modal_content}")
    
    # Check Inputs
    inputs = await page.evaluate("""() => {
         return Array.from(document.querySelectorAll('input')).map(i => i.outerHTML);
    }""")
    print(f"\nTotal Inputs on page: {len(inputs)}")
    for i in inputs:
        print(f"Input: {i}")

