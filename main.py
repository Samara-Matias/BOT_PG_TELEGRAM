from os import getenv
from PIL import Image
from PIL import ImageColor
from colorharmonies import Color, complementaryColor, triadicColor, splitComplementaryColor, tetradicColor, analogousColor, monochromaticColor
import PIL
import telebot
from telebot import types
import dotenv
import randomcolor
# ------------------------------------------------------------------------

dotenv.load_dotenv()
botAPIKey = getenv("PC_BOTKEY")

# Inicializando o bot
bot = telebot.TeleBot(botAPIKey)

# Funções:

def criar_paleta_aleatoria(qtd_cores: int):
    """
    Essa função é responsável por retornar um Array com a quantidade de cores desejada pelo usuário.

    Args:

        qtd_cores (int): Quantidade de cores que  devem ser geradas.

    Returns:
        Array com as cores criadas
    """
    paleta = (randomcolor.RandomColor()).generate(count=qtd_cores)
    # As cores geradas são em HEX
    return paleta

def criar_img_paleta(largura, altura, cor):
    """
    Descrição:
        Função que possibilita a criação de uma imagem simples, apenas com algum formato e uma cor de fundo.

    Args:
        largura: Recebe a largura da imagem (será considerado, pela função, como valor em PX).
        altura: Recebe a altura da imagem (valor considerado como PX pela pessoa).
        cor: Recebe como valor uma cor para ser utilizado como plano de fundo da imagema ser criada.

    Returns:
        Imagem criada
    """
    img = PIL.Image.new(mode='RGB', size=(largura, altura), color=(cor))
    return img

def hex_to_rgb(cores):
    """
    Descrição:
        Função que converte uma cor em Hexadecimal para uma cor no formato RGB.

    Args:
        cores: array contendo as cores em Hexadecimal e que serão convertidas em RBG
    Returns:
        Array com cores convertidas para RBG
    """
    cores_ = []
    for cor in cores:
        cores_.append(ImageColor.getrgb(cor))
    return cores_

def rgb_to_hex(cor):
    """
    Descrição:
        Função para converter uma cor em RGB para Hexadecial.
    Args:
        cor: array contendo a cor em RGB e que será convertido em Hexadecimal
    Returns:
        String contendo a cor em Hexadecimal
    """
    cor_hex = '#{:02x}{:02x}{:02x}'.format(cor[0], cor[1], cor[2])
    return cor_hex

def returnInstanciaCH(cor):
    """
    Descrição:
        Função para criação de instancias da classe 'Color' da biblioteca 'coloharmonies' e, assim, poder utilizar os métodos presentes nela
    Args:
        cor(array): Array contento a cor para criação do objeto 'Color'
    Returns:
        Array com o objeto 'Color'
    """
    cor_ch = []
    for i in range(3):
        cor_ch.append(cor[0][i])
    return Color(cor_ch, "", "")

def gerar_esquema_complementar(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema da Cor Complementar, em RGB, da cor fornecida.
        - Definição de esquema complementar: Usa cores opostas no círculo cromático, como vermelho e verde, azul e laranja. Essas combinações criam um contraste forte e vibrante, sendo ideal para destacar elementos específicos.

    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com a core formada, no formato RGB.
    """
    return complementaryColor(returnInstanciaCH(cor))

def gerar_esquema_triade(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema das Cores Triádes, em RGB, da cor fornecida.
        - Definição de esquema triádico: sa três cores igualmente espaçadas no círculo cromático, como verde, laranja e roxo. Oferece um equilíbrio entre contraste e harmonia, permitindo uma paleta vibrante sem ser tão intensa quanto a complementar.

    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com as cores formadas, no formato RGB.
    """
    return triadicColor(returnInstanciaCH(cor))

def gerar_esquema_monocromatico(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema das Cores Monocromáticas, em RGB, da cor fornecida.
        - Definição de esquema monocromático: Baseia-se em uma única cor em diferentes tonalidades, incluindo variações mais claras e mais escuras da mesma cor. É simples e cria uma sensação de harmonia e serenidade.
    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com as cores formadas, no formato RGB.
    """
    return monochromaticColor(returnInstanciaCH(cor))

def gerar_esquema_complementar_dividido(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema das Cores Complementares Divididas, em RGB, da cor fornecida.
        - Definição de esquema complementar dividido: Escolhe uma cor principal e as duas cores ao lado de seu complementar. Por exemplo, verde, vermelho-violeta e vermelho-alaranjado. Oferece um contraste mais suave que o complementar direto.
    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com as cores formadas, no formato RGB.
    """
    return splitComplementaryColor(returnInstanciaCH(cor))

def gerar_esquema_analogo(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema das Cores Análogas, em RGB, da cor fornecida.
        - Definição de esquema análogo: Usa cores adjacentes no círculo cromático. Por exemplo, tons de azul, verde e turquesa. É uma escolha natural e suave, ideal para criar uma sensação de conforto e coesão.
    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com as cores formadas, no formato RGB.
    """
    return analogousColor(returnInstanciaCH(cor))

def gerar_esquema_tetradico(cor):
    """
    Descrição:
        Função para gerar um array com cores do esquema das Cores Tetradrica, em RGB, da cor fornecida.
        - Definição de esquema tetradrico: Usa duas combinações de cores complementares. Por exemplo, vermelho com verde e amarelo com roxo. Proporciona um alto contraste.
    Args:
        cor(array): Array com a cor base para criação do esquema.
    Returns:
        Array com as cores formadas, no formato RGB.
    """
    return tetradicColor(returnInstanciaCH(cor))



# => Funcionalidades do BOT <=

@bot.message_handler(func= lambda msg: msg.text == "/start" or msg.text == "Retornar para as opções iniciais")
def mensagem_inicial_retorno(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    opc_criar_paleta = types.KeyboardButton('Criar uma paleta de cores')
    opc_retornar_opcoes = types.KeyboardButton('Opções de escolha')

    markup.add(opc_criar_paleta, opc_retornar_opcoes)
    bot.send_message(msg.chat.id, f"Selecione alguma das opções abaixo expostas na área do teclado", reply_markup=markup)

@bot.message_handler(func= lambda msg: msg.text == "Criar uma paleta de cores")
def criar_paleta_opc(msg):
    if msg.text == 'Criar uma paleta de cores':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        gerar_1 = types.KeyboardButton('Gerar uma cor')
        gerar_2 = types.KeyboardButton('Gerar duas cores')
        gerar_3 = types.KeyboardButton('Gerar três cores')
        gerar_4 = types.KeyboardButton('Gerar quatro cores')
        gerar_5 = types.KeyboardButton('Gerar cinco cores')
        opcoes = types.KeyboardButton('Retornar para as opções iniciais')

        markup.add(gerar_1, gerar_2, gerar_3, gerar_4, gerar_5, opcoes)

        bot.send_message(msg.chat.id, f"Ok! Vamos criar uma paleta de cores ou apenas uma cor aleatória. Selecione alguma das opções abaixo:", reply_markup=markup)

@bot.message_handler(func= lambda msg: msg.text == 'Retornar para as opções iniciais')
def retorno_opc(msg):
    bot.reply_to(msg, f"Selecione alguma das opções abaixo:\n\n/{comandos[2]} - Gerar uma paleta de cores\n/{comandos[1]} - Retornar para as opções de escolha.")

# Variável para armazenar a cor única que será gerada e utilizada para gerar os esquemas
cor_gerada = ''

@bot.message_handler(func= lambda msg: msg.text == "Gerar uma cor" or msg.text == "Gerar duas cores" or msg.text == "Gerar três cores" or msg.text == "Gerar quatro cores" or msg.text == "Gerar cinco cores")
def gerar_paleta(msg):
    dic_qtd_cores = {
        "Gerar uma cor": 1,
        "Gerar duas cores": 2,
        "Gerar três cores": 3,
        "Gerar quatro cores": 4,
        "Gerar cinco cores": 5
    }
    qtd_cores = dic_qtd_cores[msg.text] 
    paleta = criar_paleta_aleatoria(qtd_cores)
    largura = 150
    altura = 150
    if(qtd_cores > 1):
        bot.send_message(msg.chat.id, f"Cores geradas:")
    else:
        bot.send_message(msg.chat.id, f"Cor gerada:")
    for i in range(qtd_cores):
            img = criar_img_paleta(largura, altura, paleta[i])
            bot.send_photo(msg.chat.id, img)
            bot.send_message(msg.chat.id, f"HEX: {paleta[i].upper()}")
    if qtd_cores == 1:
        global cor_gerada 
        cor_gerada = paleta[0]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        gerar_esq_comp = types.KeyboardButton('Gerar esquema de cor complementar')
        gerar_esq_triad = types.KeyboardButton('Gerar esquema de cores tríades')
        gerar_esq_mono = types.KeyboardButton('Gerar esquema de cores monocromático')
        gerar_esq_comp_div = types.KeyboardButton('Gerar esquema de cores complementares dividido')
        gerar_esq_analog = types.KeyboardButton('Gerar esquema de cores análogas')
        gerar_esq_tetrad = types.KeyboardButton('Gerar esquema de cor tetrádicas')
        retornar_opcoes = types.KeyboardButton('Retornar para as opções iniciais')
        markup.add(gerar_esq_comp, gerar_esq_triad, gerar_esq_mono, gerar_esq_comp_div, gerar_esq_analog, gerar_esq_tetrad, retornar_opcoes)
        bot.send_message(msg.chat.id, "Desaja realizar algumas das funções abaixo? Só escolher", reply_markup=markup)
    
# Vídeo utilizado: https://www.youtube.com/watch?v=a_f97Qoy9C4

@bot.message_handler(func= lambda msg: msg.text == "Gerar esquema de cor complementar" or msg.text == "Gerar esquema de cores tríades" or msg.text == "Gerar esquema de cores monocromático" or msg.text == "Gerar esquema de cores complementares dividido" or msg.text == "Gerar esquema de cores análogas" or msg.text == "Gerar esquema de cor tetrádicas")
def gerar_esquema_cor(msg):
    global cor_gerada
    arr_cor = []
    arr_cor.append(cor_gerada)
    cor_gerada_rgb = hex_to_rgb(arr_cor)
    largura = 150
    altura = 150
    
    cores_geradas_esq = ()
    if(msg.text == "Gerar esquema de cor complementar"):
        cores_geradas_esq =  tuple(gerar_esquema_complementar(cor_gerada_rgb))
        img = criar_img_paleta(largura, altura, cores_geradas_esq)
        bot.send_photo(msg.chat.id, img)
        bot.send_message(msg.chat.id, f"HEX: {rgb_to_hex(cores_geradas_esq)}")
        
    elif (msg.text == "Gerar esquema de cores tríades"):
        cores_geradas_esq = gerar_esquema_triade(cor_gerada_rgb)
        
    elif (msg.text == "Gerar esquema de cores monocromático"):
        cores_geradas_esq = gerar_esquema_monocromatico(cor_gerada_rgb)
    elif (msg.text == "Gerar esquema de cores complementares dividido"):
        cores_geradas_esq = gerar_esquema_complementar_dividido(cor_gerada_rgb)
    elif (msg.text == "Gerar esquema de cores análogas"):
        cores_geradas_esq = gerar_esquema_analogo(cor_gerada_rgb)
    else:
        cores_geradas_esq = gerar_esquema_tetradico(cor_gerada_rgb)

    if (msg.text != "Gerar esquema de cor complementar"):
        # cores_geradas_esq_2 = tuple(cores_geradas_esq)
        # bot.send_message(msg.chat.id, f"a: {tuple(cores_geradas_esq[0])}")
        for i in range(len(cores_geradas_esq)):
            img = criar_img_paleta(largura, altura, tuple(cores_geradas_esq[i]))
            bot.send_photo(msg.chat.id, img)
            bot.send_message(msg.chat.id, f"HEX: {rgb_to_hex(cores_geradas_esq[i]).upper()}")



bot.polling()
