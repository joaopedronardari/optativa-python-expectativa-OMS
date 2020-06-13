# DADOS DE EXPECTATIVA DE VIDA AO NASCIMENTO
# JOÃO PEDRO NARDARI DOS SANTOS

# Método criado para resolver casos com 1 valor e caso RWANDA (dois valores na mesma célula)
def getFloatNumbers(stringCSV):
    text = stringCSV.replace('"', '')

    # Resolvendo caso RWANDA
    if (" " in stringCSV):
        return [float(i) for i in text.split(" ")]
    else:
        return [float(text)]

def leituraArquivo(caminho):
    # Seleciona arquivo
    arquivo = open(caminho)

    # Primeira e segunda linha -> Cabecalhos
    arquivo.readline()
    arquivo.readline()

    linha = arquivo.readline()
    pais = ''
    listaPaises2 = []
    listaPaises = []
    todosValoresIdade = []

    maiorPais = {'nome': '', 'media': 0}
    somatorio = 0
    n = 0
    while(linha):
        partes = linha.split(',')
        if (pais != partes[0]): # Pais novo
            # Media do ultimo
            if (pais != ''):
                mediaUltimo = somatorio / n

                if (mediaUltimo > maiorPais['media']):
                    maiorPais['media'] = mediaUltimo
                    maiorPais['nome'] = listaPaises[-1]

            pais = partes[0]
            # Primeira vez que mudou o pais
            somatorio = float(partes[2].replace('"',''))
            n = 1
            listaPaises.append(partes[0].replace('"', ''))

            item = {
                "pais": partes[0].replace('"', ''),
                "valores": getFloatNumbers(partes[2])
            }

            listaPaises2.append(item)
        else: # Mesmo pais
            somatorio += float(partes[2].replace('"',''))
            n += 1
            item["valores"].extend(getFloatNumbers(partes[2]))

        todosValoresIdade.extend(getFloatNumbers(partes[2]))
        linha = arquivo.readline()

    print("Média total de idades: %f" % media(todosValoresIdade))
    print("Desvio total de idades: %f" % desvio(todosValoresIdade))
    
    print("O Maior país é: " + maiorPais['nome'] + " com média " + str(maiorPais['media']))

    return listaPaises2

def media(valores):
    soma = 0
    for valor in valores:
        soma += valor
    return soma / len(valores)

def desvio(valores):
    avg = media(valores)
    somatoria = 0
    for valor in valores:
        somatoria += (valor - avg) ** 2
    return (somatoria / len(valores)) ** (1/2)

def main():
    listaPaises = leituraArquivo('./dataoms.csv')

    menorExpectativa = {'pais': '', 'media': media(listaPaises[0]['valores'])}
    maiorExpectativa = {'pais': '', 'media': 0}
    
    # Iterando lista de países
    with open('./resultados.csv', 'w') as resultadosCsv:
        resultadosCsv.write("Pais,Media,Desvio\n")
        
        for i in listaPaises:
            avg = media(i['valores'])

            # Verificação maior / menor
            if avg > maiorExpectativa['media']:
                maiorExpectativa['pais'] = i['pais']
                maiorExpectativa['media'] = avg  
            if avg < menorExpectativa['media']:
                menorExpectativa['pais'] = i['pais']
                menorExpectativa['media'] = avg
            
            # Escreve linha do país no arquivo
            resultadosCsv.write("%s,%f,%f\n" % (i['pais'],avg,desvio(i['valores'])))

    print("Maior expectativa: %s %f" % (maiorExpectativa['pais'],maiorExpectativa['media']))
    print("Menor expectativa: %s %f" % (menorExpectativa['pais'],menorExpectativa['media']))

if __name__=="__main__":
    main()