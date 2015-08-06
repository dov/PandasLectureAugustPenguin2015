GroupBy objects are iteratable

markdown:
We can loop through a groupby object to get the index and the DataFrame:

In [ ]:
port_names = {'C':'Cherbourg','Q':'Queenstown','S': 'Southampton'}
for (port,sex), group in df.groupby(['Embarked','Sex']):
  print 'Embarked at', port_names[port],':', sex
  print group.Survived.sum(), 'survived out of', group.Survived.count()
  


