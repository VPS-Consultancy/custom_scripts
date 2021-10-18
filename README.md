## Custom Scripts

For custom scripts

Inches Task:
Disable hidden, readonly - Itemgroup (Sales Invoice Item)

Override Core:

taxes_and_totals.js
```
if(item.inches)
{
  item.qty=item.inches*0.00694444;
}
 ```

taxes_and_totals.py
``` 
if item.inches:
  item.qty=item.inches*0.00694444
```

#### License

MIT
