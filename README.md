## Custom Scripts

For custom scripts

Inches Task:
Disable hidden, readonly - Itemgroup (Sales Invoice Item)

Override Core:

taxes_and_totals.js
```
if(item.inches>0 && item.inches<=3){
					item.qty=item.inches*0.00694444;
				}
				else{
					const object = {1: [1,3], 6:[3,6], 9:[6,9], 12:[9,12],
						16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
						72:[60,72], 84:[72, 84], 96:[84, 96]
						};
					for (const [key, value] of Object.entries(object)) {
						if(item.inches>value[0] && item.inches<=value[1]){
							item.qty=key*0.00694444;
						}
		
					}
				}
 ```

taxes_and_totals.py
``` 
if(item.get('inches')>0 and item.get('inches')<=3):
					item.qty=item.inches*0.00694444
				else:
					intervals = {1: [1,3], 6:[3,6], 9:[6,9], 12:[9,12],
					16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
					72:[60,72], 84:[72, 84], 96:[84, 96]
					}
					for key in intervals:
						if item.get('inches')>intervals[key][0] and item.get('inches')<=intervals[key][1]:
							item.qty=key*0.00694444
```

#### License

MIT
