## Custom Scripts

For custom scripts

Inches Task:
Disable hidden, readonly - Itemgroup (Sales Invoice Item)

Override Core:

taxes_and_totals.js
```
var inches = 0;
if (item.height) {
		const object = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
		16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
		72:[60,72], 84:[72, 84], 96:[84, 96]
		};
		for (const [key, value] of Object.entries(object)) {
			if(item.height>value[0] && item.height<=value[1]){
				if (item.inches!==0)
				{
					if(item.weight!==0){
						for (const [key1, value1] of Object.entries(object)) {
							if(item.weight>value1[0] && item.weight<=value1[1]){
								inches = key * key1;
							}

						}
					}
				}
				else{
					inches = key;
				}
			}

		}
		item.inches =  inches;
}
if (item.weight) {
			const object = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
			16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
			72:[60,72], 84:[72, 84], 96:[84, 96]
			};
			for (const [key2, value2] of Object.entries(object)) {
				if(item.weight>value2[0] && item.weight<=value2[1]){
					if (item.inches!==0)
					{
						if(item.height!==0){
							for (const [key3, value3] of Object.entries(object)) {
								if(item.height>value3[0] && item.height<=value3[1]){
									inches = key2 * key3;
								}

							}
						}
					}
					else{
						inches = key2;
					}
				}

			}
			item.inches =  inches;
	}
item.qty = inches * 0.00694444;
 ```

taxes_and_totals.py
``` 
inches = 0
if item.get('height'):
	intervals = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
	16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
	72:[60,72], 84:[72, 84], 96:[84, 96]
	}
	for key in intervals:
		if item.get('height')>intervals[key][0] and item.get('height')<=intervals[key][1]:
			if item.get('inches')!=0:
				if item.get('weight')!=0:
					for key1 in intervals:
						if item.get('weight')>intervals[key1][0] and item.get('weight')<=intervals[key1][1]:
							inches = key * key1
			else:
				inches = key
	item.inches =  inches

if item.get('weight'):
	intervals = {3: [0,3], 6:[3,6], 9:[6,9], 12:[9,12],
	16:[12,16], 18:[16,18], 21:[18,21], 24:[21,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
	72:[60,72], 84:[72, 84], 96:[84, 96]
	}
	for key in intervals:
		if item.get('weight')>intervals[key][0] and item.get('weight')<=intervals[key][1]:
			if item.get('inches')!=0:
				if item.get('height')!=0:
					for key1 in intervals:
						if item.get('height')>intervals[key1][0] and item.get('height')<=intervals[key1][1]:
							inches = key * key1
			else:
				inches = key
	item.inches =  inches
item.qty = inches * 0.00694444
```

#### License

MIT
