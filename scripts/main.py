# ============================================================
# Etapa de Teste - Abrir o AVA IFMS
# ============================================================

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Abre o navegador Chromium visível
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Abre o site do AVA IFMS
        page.goto("https://ead.ifms.edu.br/", wait_until="domcontentloaded")

        # Espera 3 segundos para visualização
        page.wait_for_timeout(3000)

        print("✅ Página do AVA aberta com sucesso!")

        browser.close()

if __name__ == "__main__":
    main()
