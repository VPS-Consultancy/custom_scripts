## Custom Scripts

For custom scripts

Inches Task:
Disable hidden, readonly - Itemgroup (Sales Invoice Item)

Refer Backup.js file

Override Core:

taxes_and_totals.js
```
var inches = 0;
if (item.height) {
		const object = {'Regular Moving Glass': {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
				18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
				72:[60,72], 84:[72, 84], 96:[84, 96]
				}, 'Non-Regular Moving Glass': {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:							[60,72]}};
		for (const [key, value] of Object.entries(object[item.item_group])) {
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
		const object = {'Regular Moving Glass': {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
				18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
				72:[60,72], 84:[72, 84], 96:[84, 96]
				}, 'Non-Regular Moving Glass': {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:							[60,72]}};
			for (const [key2, value2] of Object.entries(object[item.item_group])) {
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
if (inches){
	item.qty = inches * 0.00694444 * item.no_of_pieces;
}
 ```

taxes_and_totals.py
``` 
inches = 0
if item.get('height'):
	if item.get('item_group') == 'Regular Moving Glass':
		intervals = {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
		18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
		72:[60,72], 84:[72, 84], 96:[84, 96]
		}
	if item.get('item_group') == 'Non-Regular Moving Glass':
		intervals = {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:[60,72]}
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
	if item.get('item_group') == 'Regular Moving Glass':
		intervals = {3: [0,3], 6:[3,6], 12:[6,12], 15:[12,15],
		18:[15,18], 24:[18,24],30:[24,30], 36:[30,36], 42:[36,42], 48:[42,48], 60:[48,60],
		72:[60,72], 84:[72, 84], 96:[84, 96]
		}
	if item.get('item_group') == 'Non-Regular Moving Glass':
		intervals = {12:[0,12], 18:[12,18], 24:[18,24], 36:[24,36], 48:[36,48], 60:[48,60], 72:[60,72]}
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

if inches:
	item.qty = inches * 0.00694444 * item.no_of_pieces
```

#### License

MIT
