import React, {useState, useEffect} from 'react';
import { StyleSheet, View, Text, ScrollView} from 'react-native';
import {Icon, useTheme, Button, List} from 'react-native-paper';
import Page from './Page.js'


export default function Link() {
    const theme = useTheme();
    const styles = StyleSheet.create({
       body :{
        height: '100%',
        width: '100%',
        flex: 1,
        alignItems: 'center',
        top: '15%',
       },
       bodyTXT: {
        top: '5%',
        marginBottom: '5%',
        fontSize: 30,
        textAlign: 'center',
        color: theme.colors.primary,
       },
       bodysubTXT: {
        top: '5%',
        bottom: '15%',
        fontSize: 18,
        textAlign: 'center',
        color: theme.colors.secondary,
       },
       list: {
       },
       scrollView: {
        width: '100%',
      },
      listContainer: {
        marginTop: '5%',
        paddingTop: '5%',
        alignItems: 'center',
        flex: 1,
      },
      buttonContainer: {
        alignSelf: 'center',
        alignItems: 'flex-start',
        justifyContent: 'center',
        top: '5%',
        marginBottom: '5%',
        },
    });
    const bodyContent =(
    <View style={styles.body}>
        <Icon
        source="cellphone-link"
        size={160}/>
        <Text style={styles.bodyTXT}>Use APP on web {'\n'}desktop, and other devices</Text>
        <View style={styles.listContainer}>
        <ScrollView style={styles.scrollView}>
        <Button 
          mode="elevated" 
          style={styles.buttonContainer} 
          onPress={() => console.log('Pressed')}>
          <Text style={styles.menuText}>Add a New Device</Text>
        </Button>
          <List.Section style={styles.list}>
            <List.Subheader style ={styles.bodysubTXT}>Current Devices</List.Subheader>
            <List.Item title="First Item" left={() => <List.Icon icon="folder" />} />
            <List.Item
              title="Second Item"
              left={() => <List.Icon color={theme.colors.tertiary70} icon="folder" />}
            />
          </List.Section>
        </ScrollView>
        </View>
        </View>
    );
    return (
        <Page TITLE='Linked Devices' bodyContent={bodyContent} />
        )
}
