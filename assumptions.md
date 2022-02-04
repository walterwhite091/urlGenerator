#### Assumptions:
1. Formatter will not format alphanumeric values
2. https://HOST_NAME/<short_hash_string>
    length of **short_hash_string**  is 1-6
3. Shorten URL will be **one time** use only
4. Alphanumeric chars will be :
    a--z == 26
    A--Z == 26
    0--9 ==  9
    total = 62
    latin chars like  Å , å , Ǻ will not treated as alphanumeric 