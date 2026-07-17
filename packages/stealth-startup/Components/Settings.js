import React, {useState, useEffect} from 'react';
import { StyleSheet, View, Text, Image, Switch, TouchableOpacity, ScrollView } from 'react-native';
import { Avatar, Button, Card, useTheme, Searchbar } from 'react-native-paper';
import Page from './Page.js';
import { useNavigation } from '@react-navigation/native';

export default function Settings() {
  const [searchQuery, setSearchQuery] = React.useState('');
  const navigation = useNavigation();
  const onChangeSearch = query => setSearchQuery(query);
  const theme = useTheme();
  const styles = StyleSheet.create({
    buttonList:{
    width: '100%',
    flexShrink:1,
    elevation: 5,
    alignItems: 'center', 
  },
  buttonContainer: {
   rippleWidth: '100%',
   width: '80%',
   height: 100,
   alignSelf: 'center',
   alignItems: 'flex-start',
   justifyContent: 'center',
   marginTop: '1.25%',
   marginBottom: '1.25%',
},
  	menuText: {
    position: 'relative',
    flexShrink: 0,
    flex: 1,
    flexDirection: "column",
    left: 20,
    fontSize: 18,
    fontWeight: "400",
    letterSpacing: 0
},
footertxt: {
  position: 'relative',
  flex: 1,
  flexDirection: 'column',
  fontSize: 12,
  alignSelf: 'center',
  justifyContent: 'flex-end',
},
  infocontainer: {
    flexDirection: 'row',
     width: '100%',
     height: '12.5%',
     alignItems: 'center', 
     justifyContent: 'center', 
     top: '5%', 
     marginBottom: '5%',
     paddingBottom: '10%',
     alignSelf: 'flex-start',
     elevation: 15,
    shadowColor: 'black',
    shadowOffset: { width: 0, height: 3 },
    shadowRadius: 3.84,
    right:5,
    shadowOpacity: 1,
    },
  bizname: {
    color: theme.colors.primary,
    fontSize: 18,
    fontWeight: 'bold',
    left: 5,
    right: -5,
    
  },
  pfp: {
    left: -5,
    elevation: 5,
    shadowColor: 'black',
    shadowOffset: { width: 0, height: 0 },
    shadowRadius: 3.84,
    right:5,
    shadowOpacity: 0.5,
  },
  scrollView: {
    width: '100%',
    paddingTop: '5%',
  }
})
  const screens = [
    {name: 'Starred Contacts', icon: 'star', component: 'Star'},
    {name: 'Linked Devices', icon: 'cellphone-link', component: 'Link'},
    {name: 'Account', icon: 'account', component: 'Account'},
    {name: 'Privacy', icon: 'eye', component: 'Privacy'},
    {name: 'Notifications', icon: 'bell', component: 'Notifications'},
    {name: 'Downloads', icon: 'download', component: 'Downloads'},
    {name: 'Help', icon: 'help-circle', component: 'Support'},
    {name: 'Tell A Friend', icon: 'share-variant', component: 'TellAFriend'},

  ];
  const bodyContent = (
    <View>
    <ScrollView style={styles.scrollView}>
    <View style= {styles.infocontainer}>
    <Avatar.Icon style={styles.pfp} size={64} icon="folder" />
    <Text style={styles.bizname}>NAME OF BUSINESS</Text>
    </View>
    
      <View style={styles.buttonList} >
        {screens.map((screen, index) => (
        <Button 
          key={index}
          icon={screen.icon} 
          mode="elevated" 
          style={styles.buttonContainer} 
          onPress={() => navigation.navigate('SettingsTab', { screen: screen.name })}>
          
          <Text style={styles.menuText}>{screen.name}</Text>
        </Button>
      ))}
      <Text style={styles.footertxt}>Version 1.0.0</Text>
    </View>
    <View style={{height:200, width:'100%',}} />
    </ScrollView>
  </View>
  );
    return (
       
    		<Page TITLE='Settings'  bodyContent={bodyContent} navigation={navigation} useNav={true} useSearch={true}>
            
      		</Page>
    )
}



