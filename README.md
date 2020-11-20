fetch the price of an amazon product and compare it to a wanted price.
uses sqlite3.

## install:
```console
pip install .
```

## run:
### add item:
```console
ap add $ID $WANTED_PRICE
```
### example:
```console
ap add B07RSSH31R 28
```

### list your items:
```console
ap ls
```
### example:
```console
root@bear:~# ap ls
listing products:
+----+--------------+----------------+--------------------+--------+
|    |  product_id  |   price_wanted |   prices_last_seen |  buy?  |
|----+--------------+----------------+--------------------+--------|
|  0 |  B07KW97DW6  |             16 |              16.99 |        |
|  1 |  B0748KLR39  |             18 |              17.54 |   x    |
|  2 |  B0827X2RQV  |             10 |             nan    |        |
|  3 |  B0000WPM4W  |              8 |               8.21 |        |
+----+--------------+----------------+--------------------+--------+
```