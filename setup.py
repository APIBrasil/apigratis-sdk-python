from setuptools import setup

setup(
    name='apigratis',
    version='0.0.9',
    description='Transforme seus projetos em soluções inteligentes com nossa API. Com recursos como  API do WhatsApp, geolocalização, rastreamento de encomendas, verificação de CPF/CNPJ e mais, você pode criar soluções eficientes e funcionais. Comece agora.',
    author='APIBRASIL',
    author_email='contato@apibrasil.com.br',
    packages=['apigratis'],
    install_requires=[
        # Lista de dependências necessárias
        'requests',
    ],
)