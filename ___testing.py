import sys
from time import sleep
from WhatsAppWeb.WhatsAppWeb import WhatsAppWeb as wap
from selenium.webdriver.common.keys import Keys
w = wap()
w.open_red_robot_chat(timeout=60)
chat = w.find_element_by_id("main")
type_a_msg = chat.find_element_by_css_selector("div._13NKt.copyable-text.selectable-text")
type_a_msg.send_keys("Oi, tudo bem?")
type_a_msg.send_keys(Keys.ENTER)
sleep(15)

sys.exit()

side_panel = w.find_element_by_id("side")
chat_window = w.find_element_by_id("main")

chats = side_panel.find_elements_by_class_name("_3m_Xw")

chat_subject = w.find_element_by_class_name("ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr")[0].innerHTML
new_message_green_circle = w.find_element_by_class_name("l7jjieqr cfzgl7ar ei5e7seu h0viaqh7 tpmajp1w c0uhu3dl riy2oczp dsh4tgtl sy6s5v3r gz7w46tb lyutrhe2 qfejxiq4 fewfhwl7 ovhn1urg ap18qm3b ikwl5qvt j90th5db aumms1qt")
emoji_robozinho = "b95 emoji wa i0jNr 🤖"

for chat in chats:
    print(chat.find_element_by_class_name("ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr").innerHTML)
