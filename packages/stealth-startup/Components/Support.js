import React, {useState, useEffect} from 'react';
import { StyleSheet, View, Text, Image, Switch, TouchableOpacity } from 'react-native';
import {Icon, useTheme, Button} from 'react-native-paper';
import Page from './Page.js'


export default function Support() {
    const theme = useTheme();
    const styles = StyleSheet.create({
       support :{
        height: '100%',
        width: '100%',
        flex: 1,
        alignItems: 'center',
        top: '15%'
       },
       supTXT: {
        top: '5%',
        fontSize: 30,
        color: theme.colors.primary,
       },
       supsubTXT: {
        top: '5%',
        fontSize: 12,
        color: theme.colors.secondary,
       },
         buttonContainer: {
            rippleWidth: '100%',
            width: '80%',
            height: 100,
            alignSelf: 'center',
            alignItems: 'flex-start',
            justifyContent: 'center',
            top: '25%',
            marginTop: '1.25%',
            marginBottom: '1.25%',
            },
    });
    const bodyContent =(
    <View style={styles.support}>
        <Icon
        source="headset"
        size={160}/>
        <Text style={styles.supTXT}>Need Help?</Text>
        <Text style ={styles.supsubTXT}>Submit a ticket below</Text>
        <Button 
          mode="elevated" 
          style={styles.buttonContainer} 
          onPress={() => console.log('Pressed')}>
          <Text style={styles.menuText}>Contact Us</Text>
        </Button>
        </View>
    );
    return (
        <Page TITLE='Support' useNav='false' useSearch='false' bodyContent={bodyContent} />
        )
}