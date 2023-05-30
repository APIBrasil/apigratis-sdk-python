from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='apigratis',
    version='0.0.1',
    url='https://github.com/caiocarneloz/apigratis',
    license='MIT License',
    author='Caio Carneloz',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='contato@apibrasil.com.br',
    keywords='whatsapp api, apibrasil, cnpj, sms, cep, consulta, api, brasil, gratis, free, whatsapp, apiwhatsapp, apigratis, apifree',
    description=u'Transforme seus projetos em soluções inteligentes com nossa API. Com recursos como API do WhatsApp, geolocalização, rastreamento de encomendas, verificação de CPF/CNPJ e mais, você pode criar soluções eficientes e funcionais',
    packages=['apigratis'],
    install_requires=['numpy'],)