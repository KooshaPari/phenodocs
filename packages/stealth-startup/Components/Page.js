import React, { useState } from 'react';
import { StyleSheet, View, Platform, Image, Switch, TouchableOpacity } from 'react-native';
import { useTheme, Appbar, BottomNavigation, Text,} from 'react-native-paper';

function Page({bodyContent, ...props})  {
  const theme = useTheme();
  const styles = StyleSheet.create({
    page: {
      width:'100%',
      height: '100%',
      backgroundColor: theme.colors.primary,
    },
    body: {
      flex:1,
      backgroundColor: theme.colors.background,
      width: '100%',
     // height: '77%',
    },
  });
  

  return (
    <View style={styles.page}>
      <View style={styles.body}>
        {bodyContent}
      </View>
     </View>
    
  );
};

export default Page;