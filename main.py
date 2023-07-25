from hex_domain import HexDomain

domain = HexDomain(2)
domain.gridpoints = domain.in_hex()
domain.draw()

#domain = HexDomain(10)
#domain.fill_min()
#domain.sample(iters=100000)
#domain.draw(show_grid=False)
