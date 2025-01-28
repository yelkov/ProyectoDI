#styles.py
def load_stylesheet():
    '''

    :return: boolean
    Carga y devuelve el contenido de styles.qss como una cadena
    '''

    with open('styles.qss', 'r') as style_file:
        return style_file.read()