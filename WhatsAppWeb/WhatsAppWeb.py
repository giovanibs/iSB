# WebWhatsApp Class
import inspect
from selenium.webdriver import Chrome
import os
from time import time, sleep

class WhatsAppWeb(Chrome):
    """
    Cria novo driver do chrome e possui métodos para converter moedas.
    """

    def __init__(self, driver_path="C:\SeleniumDrivers", teardown=True):
        """
        Cria nova instância da classe WhatsAppWeb. Adiciona a pasta com 
        drivers no PATH (variáveis de ambiente)

        IMPORTANTE: comentar a respectiva linha no método __init__ caso não seja 
        necessário adicionar o caminho dos drivers no PATH (variáveis de ambiente).
        
        Parâmetros
        ----------
            driver_path (str): Caminho onde estão salvos os drivers dos navegadores (pode ser alterado nas contantes)
            
            teardown (bool): Flag utilizada no método __exit__
        """
        self.BASE_URL = r"https://web.whatsapp.com/"
        self.driver_path = driver_path
        self.teardown = teardown

        # COMENTAR A LINHA ABAIXO SE NÃO PRECISAR ALTERAR O PATH NAS VARIÁVEIS DE AMBIENTE
        os.environ["PATH"] += os.pathsep + self.driver_path

        # cria instância da classe webdriver.Chrome para ter acesso a todos os seus métodos
        super(WhatsAppWeb, self).__init__()

        self.implicitly_wait(5)

    def __exit__(self):
        """Fecha a webpage caso o atributo `teardown` da instância seja `True`.
        """
        if self.teardown:
            self.quit()

    def open_red_robot_chat(self, timeout=30):
        this_func = inspect.stack()[0][3]
        if self.current_url == self.BASE_URL:
            return
        try:
            self.get(self.BASE_URL)
        except Exception as e:
            print(
                f"**********************{e}***Erro ao abrir página do banco central*******************"
            )
            self.quit()
        
        ### make sure the site has loaded enough
        t0 = time()
        side_panel = 0
        while not side_panel:
            try:
                side_panel = self.find_element_by_id("side")
            
            except Exception as e:

                timer = time() - t0
                if timer > timeout:
                    print( f"\n\n{9*'#'}\nTimeout...{this_func}:\n{e}\n{9*'#'}" )
                    self.quit()
            sleep(1)
        sleep(5)
        # side panel is visible        
        if self.get_robot_chat():
            return self.got_robot_chat()
                
    def get_robot_chat(self):
        '''opens red robot chat if it's not open'''
        this_func = inspect.stack()[0][3]
        side_panel = self.find_element_by_id("side")
        
        t0 = time()
        robot_chat = 0
        while not robot_chat:
            try:
                robot_chat = side_panel.find_element_by_css_selector("img.b95.emoji.wa.i0jNr").click()
                return True
            
            except Exception as e:

                timer = time() - t0
                if timer > 10:
                    print( f"\n\n{9*'#'}\nTimeout...{this_func}:\n{e}\n{9*'#'}" )
                    self.quit()
            sleep(1)
        
    def got_robot_chat(self):
        this_func = inspect.stack()[0][3]
        
        t0 = time()
        ok_to_go = 0
        while not ok_to_go:
            
            try:
                ok_to_go = self.find_element_by_xpath("//div[@id='main']/header/div[2]/div/div/span/img")
                return True
            except Exception as e:
                timer = time() - t0
                if timer > 10:
                    f"\n\n{9*'#'}\nTimeout...{this_func}\nERRO: {e}\n{9*'#'}"
                print( f"\n\n{9*'#'}\n{this_func}:\n{e}\n{9*'#'}" )
                return False        