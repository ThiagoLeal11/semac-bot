import random
import subprocess


def read_from_file(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content


def write_on_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def calc_next_version(version):
    version = version.split('.')
    version[-1] = str(int(version[-1]) + 1)
    return '.'.join(version)


def calc_previous_version(version):
    version = version.split('.')
    version[-1] = str(int(version[-1]) - 1)
    return '.'.join(version)


def get_finished_fallback():
    return random.choice(['Prontinho, tudo finalizado.',
                          'Tudo certo, você já pode conferir a nova versão.',
                          'Estou super feliz, tudo deu certo!',
                          'Trabalho feito.',
                          'Missão comprida!',
                          'Pronto, tudo terminado.',])


def get_update_fallback(version):
    return random.choice([f'A nova versão {version} já está no ar! 🥳',
                          f'A versão {version} já está pronta e operando!',
                          f'A versão {version} está operando normalmente, como o esperado!',])


def get_error_fallback():
    return random.choice(['Vish, alguma coisa deu errado. 😵\nO erro é esse aqui:',
                          'Algo deu errado... Segue o que aconteceu:',
                          'Eita, aconteceu alguma coisa que eu não estava prevendo 🤔😳\nAqui está o erro: 👇👇👇👇👇👇',
                          'Panico! Aconteceu um imprevisto...',
                          'Ehh, talvez você queira dar uma olhada nisso, deve ser importante: 👇',
                          'Algo de errado não está certo\nDa uma olha nisso aqui:',
                          'Desculpa, mas parece que aconteceu alguma coisa:',])


def get_rollback_fallback(version):
    return random.choice([f'Eu voltei pra versão {version}.',
                          f'A versão {version} está executando novamente!',
                          f'E fica tranquilo a versão {version} já está executando!'])



def get_version_fallback(local, version):
    return random.choice([f'A versão atual do {local} é a {version}.',
                          f'Até onde eu sei, a versão atual do {local} é a {version}.',
                          f'Pelo que me lembro, a versão atual do {local} é a {version}.'])


class Executor():
    def __init__(self, bot, user_id, verbose=False):
        self.bot = bot
        self.user_id = user_id
        self.verbose = verbose

    def log(self, message):
        #print("--------"*10, "\n", message)
        self.bot.send_message(self.user_id, f'> {message}')

    def message(self, message):
        self.bot.send_message(self.user_id, message)

    def error(self, message):
        # Something went wrong
        self.bot.send_message(self.user_id, get_error_fallback())
        self.bot.send_message(self.user_id, f'> {message}')

    def run_command(self, command):
        trace = ''

        # Exec command and get terminal output.
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            trace += proc.stdout.readline().decode('utf-8', 'ignore')

        # Log to bot.
        if self.verbose:
            self.log(trace)

        # Check for errors and raise then.
        if proc.wait() > 0:
            self.error(trace)
            raise Exception