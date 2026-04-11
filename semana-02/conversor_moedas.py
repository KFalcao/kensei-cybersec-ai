def format_brl(value):
    return f'R${value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def main():
    print('Conversor de moeda: USD, BRL e JPY')
    origem = input('Informe a moeda de origem (USD, BRL ou JPY): ').strip().upper()

    if origem not in ('USD', 'BRL', 'JPY'):
        print('Moeda inválida. Use USD, BRL ou JPY.')
        return

    valor_texto = input(f'Informe o valor em {origem}: ').strip().replace(',', '.')

    try:
        valor = float(valor_texto)
    except ValueError:
        print('Valor inválido. Informe um número, como 10.50 ou 100.')
        return

    # Taxas de câmbio fixas; atualize conforme necessário
    usd_to_brl = 5.20
    usd_to_jpy = 133.50

    if origem == 'USD':
        valor_brl = valor * usd_to_brl
        valor_jpy = valor * usd_to_jpy
        print(f'{valor:.2f} USD = {format_brl(valor_brl)}')
        print(f'{valor:.2f} USD = {valor_jpy:,.2f} JPY')

    elif origem == 'BRL':
        valor_usd = valor / usd_to_brl
        valor_jpy = valor_usd * usd_to_jpy
        print(f'{format_brl(valor)} = {valor_usd:,.2f} USD')
        print(f'{format_brl(valor)} = {valor_jpy:,.2f} JPY')

    else:  # origem == 'JPY'
        valor_usd = valor / usd_to_jpy
        valor_brl = valor_usd * usd_to_brl
        print(f'{valor:,.2f} JPY = {valor_usd:,.2f} USD')
        print(f'{valor:,.2f} JPY = {format_brl(valor_brl)}')


if __name__ == '__main__':
    main()
