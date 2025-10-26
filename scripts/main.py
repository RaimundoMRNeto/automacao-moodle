# ============================================================
# Etapa de Teste - Abrir o AVA IFMS (compatível com GitHub Actions)
# ============================================================

import os  # Para acessar variáveis de ambiente
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError  # Playwright e erro de timeout

def main():  # Função principal para abrir o AVA IFMS
    with sync_playwright() as p:  # Inicia o Playwright
        # HEADLESS:
        # - No GitHub Actions (ambiente sem interface gráfica) deve ser True.
        # - Localmente você pode visualizar definindo a variável de ambiente HEADLESS=false antes de rodar.
        headless = os.getenv("HEADLESS", "true").lower() == "true"

        # Lança o Chromium. args extras ajudam em ambientes Linux/CI.
        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-gpu"]
        )

        page = browser.new_page()

        # Aumenta os timeouts para evitar erros em redes mais lentas
        page.set_default_timeout(60_000)                # Ações (click, fill, etc.)
        page.set_default_navigation_timeout(60_000)     # Navegação (goto, reload)

        try:
            # Acessa o AVA IFMS e espera o DOM principal carregar
            page.goto("https://ead.ifms.edu.br/", wait_until="domcontentloaded")

            # Garante que o <body> está presente
            page.wait_for_selector("body", timeout=60_000)

            print(f"✅ Página do AVA aberta com sucesso! (headless={headless})")

        except PlaywrightTimeoutError as e:
            # Em caso de timeout, salva um print da tela para diagnóstico
            page.screenshot(path="erro_timeout.png", full_page=True)
            print("⚠️ Timeout ao carregar a página do AVA.")
            print("   Foi salvo um screenshot: erro_timeout.png")
            print("   Detalhes:", e)

        finally:
            browser.close()  # Fecha o navegador de forma segura


if __name__ == "__main__":
    main()
