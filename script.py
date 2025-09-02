from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import ctypes
import tkinter as tk
from tkinter import simpledialog
import sys
import tkinter.messagebox as messagebox

def validar_codigo(codigo):
    # Exemplo simples: código com números, traço e tamanho mínimo 10
    if codigo is None:
        return False
    codigo = codigo.strip()
    if len(codigo) < 10:
        return False
    # Opcional: regex para validar padrão (ex: "1234567890-99")
    # if not re.match(r'^\d{10}-\d{2}$', codigo):
    #     return False
    return True

# === Obtem código por argumento ou input
if len(sys.argv) > 1:
    codigo = sys.argv[1]
else:
    root = tk.Tk()
    root.withdraw()
    codigo = simpledialog.askstring("Código SNCI", "Digite o código SNCI (ex: 081008000136-89):")

if not validar_codigo(codigo):
    print("⚠️ Código inválido ou vazio. Encerrando o script.")
    root.destroy()  # fecha a janela ocultada
    sys.exit(1)

# === CONFIGURAÇÕES FIXAS ===
url = 'https://mapa.onr.org.br/'
data_camada = 'snci_certificado'
grupo_nome = 'Imóveis Rurais'

# === OPÇÕES DO CHROME ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("detach", True)
# === INICIA O CHROME ===
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 30)
driver.get(url)
time.sleep(5)

# === ABRE DROPDOWN DE CAMADAS ===
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-busca-camada'))).click()
time.sleep(1)

# === EXPANDE O GRUPO DE CAMADAS ===
for grupo in driver.find_elements(By.CLASS_NAME, 'toggle-subnivel'):
    if grupo_nome.lower() in grupo.text.lower():
        driver.execute_script("arguments[0].click();", grupo)
        time.sleep(1)
        break

# === CLICA NA CAMADA SNCI - CERTIFICAÇÃO ===
try:
    camadas = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, f"//div[@class='dropdown-item' and @data-camada='{data_camada}']")
    ))
    for camada in camadas:
        if camada.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView(true);", camada)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", camada)
            break
except Exception as e:
    print(f" Erro ao clicar na camada '{data_camada}':", e)

# === BUSCA O CÓDIGO NO CAMPO ===
input_codigo = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geocoder-control-input')))
input_codigo.clear()
input_codigo.send_keys(codigo)
input_codigo.send_keys(Keys.ENTER)
time.sleep(2)

# === CLICA NA SUGESTÃO ===
try:
    sugestao = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".geocoder-control-suggestions div"))
    )
    sugestao.click()
except:
    pass

# === CLICA NO CENTRO DA TELA ===
time.sleep(8)
try:
    width = driver.execute_script("return window.innerWidth")
    height = driver.execute_script("return window.innerHeight")
    center_x = width // 2
    center_y = height // 2
    ActionChains(driver).move_by_offset(center_x, center_y).click().perform()
    ActionChains(driver).move_by_offset(-center_x, -center_y).perform()
except Exception as e:
    print(" Erro ao clicar no centro da tela:", e)

# Janela popup final
root = tk.Tk()
root.withdraw()                      # Oculta a janela principal
root.attributes("-topmost", True)    # Garante que o messagebox fique na frente
messagebox.showinfo("Concluído", "Consulta Finalizada\nVocê pode fechar o navegador quando quiser.")
root.destroy()


try:
    while True:
        if driver.window_handles:
            time.sleep(1)
        else:
            break
except:
    pass
