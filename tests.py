btc_positions = [{'symbol: BTC', 'margin_balance: 0.15', 'margin_position: 0.05', 'margin_frozen: 0.01'},
                 {'symbol: BTC2', 'margin_balance: 0.15', 'margin_position: 0.05', 'margin_frozen: 0.01'}]


def test(value):
    """
    value: sets of strings
    """
    d = dict(s.split(': ') for s in p)  # turn set of strings to dict
    d = sorted(d.items(), key=lambda x: x[1], reverse=True)  # reverse sort
    l = '-' * 15  # dashed line
    fin = f'{l}\n'
    for v in d:
        fin += '='.join(v)
        fin += '\n'
    fin += l
    return fin


# iterate through btc_positions
for v in btc_positions:
    text = test(v)
