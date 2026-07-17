import 'react-native-gesture-handler';
import { StyleSheet, Text, View, useColorScheme } from 'react-native';
import SettingsSC from './Components/Settings.js';
import dark from './dark.json';
import light from './light.json';
import * as React from 'react';
import Support from './Components/Support.js';
import Link from './Components/Link.js';
import Star from './Components/Star.js';
import Account from './Components/Account.js';
import Home from './Components/Home.js';
import Privacy from './Components/Privacy.js';
import Notifications from './Components/Notifications.js';
import Downloads from './Components/Downloads.js';
import TellAFriend from './Components/TellAFriend.js';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createMaterialBottomTabNavigator,  } from 'react-native-paper/react-navigation';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { getHeaderTitle } from '@react-navigation/elements';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { MD3DarkTheme as DTheme, MD3LightTheme as LTheme, Provider as PaperProvider, Icon, Appbar} from 'react-native-paper';
function NavBar({
  navigation,
  route,
  options,
  back,
})  
{
  const title = getHeaderTitle(options, route.name);
  const showSearch = route.name === 'Home' || route.name === 'Settings' || route.name === 'Profile';
  const showBackAction = route.name !== 'Home' && route.name !== 'Settings' && route.name !== 'Profile';;
  return (
    <Appbar.Header>
     {showBackAction && <Appbar.BackAction onPress={navigation.goBack} />}
      <Appbar.Content title={title} />
      {showSearch && <Appbar.Action icon="magnify" onPress={() => {}} />}
    </Appbar.Header>
  );
}
const Hscreens = [
  {name: 'Settings', component: SettingsSC},
  {name: 'Starred Contacts', component: Star},
  {name: 'Linked Devices', component: Link},
  {name: 'Account', component: Account},
  {name: 'Privacy', component: Privacy},
  {name: 'Notifications', component: Notifications},
  {name: 'Downloads', component: Downloads},
  {name: 'Help', component: Support},
  {name: 'Tell A Friend', component: TellAFriend},

];
const Pscreens = [
  {name: 'Settings', component: SettingsSC},
  {name: 'Starred Contacts', component: Star},
  {name: 'Linked Devices', component: Link},
  {name: 'Account', component: Account},
  {name: 'Privacy', component: Privacy},
  {name: 'Notifications', component: Notifications},
  {name: 'Downloads', component: Downloads},
  {name: 'Help', component: Support},
  {name: 'Tell A Friend', component: TellAFriend},

];
const Nscreens = [
  {name: 'Settings', component: SettingsSC},
  {name: 'Starred Contacts', component: Star},
  {name: 'Linked Devices', component: Link},
  {name: 'Account', component: Account},
  {name: 'Privacy', component: Privacy},
  {name: 'Notifications', component: Notifications},
  {name: 'Downloads', component: Downloads},
  {name: 'Help', component: Support},
  {name: 'Tell A Friend', component: TellAFriend},

];
const SCscreens = [
  {name: 'Settings', component: SettingsSC},
  {name: 'Starred Contacts', component: Star},
  {name: 'Linked Devices', component: Link},
  {name: 'Account', component: Account},
  {name: 'Privacy', component: Privacy},
  {name: 'Notifications', component: Notifications},
  {name: 'Downloads', component: Downloads},
  {name: 'Help', component: Support},
  {name: 'Tell A Friend', component: TellAFriend},

];
const Stack = createNativeStackNavigator();
const HomeStack = () => (
  <NavigationContainer  independent={true}>
      <Stack.Navigator initialRouteName="Home" screenOptions={{
          header: (props) => <NavBar {...props} />,
        }}>
        <Stack.Screen name="Home" component={Home} />
      </Stack.Navigator>
    </NavigationContainer>
);
const ProfileStack = () => (
  <NavigationContainer  independent={true}>
      <Stack.Navigator initialRouteName="Home" screenOptions={{
          header: (props) => <NavBar {...props} />,
        }}>
        <Stack.Screen name="Home" component={SettingsSC} />
        <Stack.Screen name="Link" component={Link} />
      </Stack.Navigator>
    </NavigationContainer>
);
const NotificationsStack = () => (
  <NavigationContainer  independent={true}>
      <Stack.Navigator initialRouteName="Home" screenOptions={{
          header: (props) => <NavBar {...props} />,
        }}>
        
        <Stack.Screen name="Home" component={SettingsSC} />
      </Stack.Navigator>
    </NavigationContainer>
);
const SettingsStack = () => (
        <Stack.Navigator initialRouteName="Home" screenOptions={{
            header: (props) => <NavBar {...props} />,
          }}>
           {SCscreens.map((screen, index) => (  <Stack.Screen  key={index} 
          name={screen.name} 
          component={screen.component}  />))}
        </Stack.Navigator>
  );
const Tab = createMaterialBottomTabNavigator();
const TabNavigator = ({theme}) => (
  <Tab.Navigator theme={theme}>
  <Tab.Screen 
    name="HomeTab" 
    component={HomeStack} 
    options={({route}) =>({
      tabBarLabel: 'Home',
      tabBarVisible: route.state ? route.state.index === 0 : true,
      tabBarIcon: ({ focused }) => (
        focused ? <MaterialCommunityIcons size={24}  color={theme.colors.tertiary}
        style={{ alignSelf: 'center' }} name="home" /> : <MaterialCommunityIcons size={24} color={theme.colors.tertiary} 
        style={{ alignSelf: 'center' }}  name="home-outline" />
      ),
    })}
  />
  <Tab.Screen 
    name="ProfileTab" 
    component={NotificationsStack} 
    options={({route}) =>({
      tabBarLabel: 'Profile',
      tabBarVisible: route.state ? route.state.index === 0 : true,
      tabBarIcon: ({ focused }) => (
        focused ? <MaterialCommunityIcons size={24} color={theme.colors.tertiary} 
        style={{ alignSelf: 'center' }} name="account" /> : <MaterialCommunityIcons color={theme.colors.tertiary} size={24} 
        style={{ alignSelf: 'center' }}  name="account-outline" />
      ),
    })}
  />
  <Tab.Screen 
    name="NotificationsTab" 
    component={Support} 
    options={({route}) =>({
      tabBarLabel: 'Notifications',
      tabBarVisible: route.state ? route.state.index === 0 : true,
      tabBarIcon: ({ focused }) => (
        focused ? <MaterialCommunityIcons size={24} 
        style={{ alignSelf: 'center' }}  name="bell" color={theme.colors.tertiary} /> : <MaterialCommunityIcons color={theme.colors.tertiary}  size={24} 
        style={{ alignSelf: 'center' }}s size={24} 
        style={{ alignSelf: 'center' }}  name="bell-outline" />
      ),
    })}
  />
  <Tab.Screen 
    name="SettingsTab" 
    component={SettingsStack} 
    options={({route}) =>({
      tabBarLabel: 'Settings',
      tabBarVisible: route.state ? route.state.index > 0 ? false : true : true,
      tabBarIcon: ({ focused }) => ( 
        focused ? <MaterialCommunityIcons size={24} color={theme.colors.tertiary} 
        style={{ alignSelf: 'center' }} name="cog" /> : <MaterialCommunityIcons size={24} color={theme.colors.tertiary} 
        style={{ alignSelf: 'center' }}  name="cog-outline" />
      ),
    })}
  />
  </Tab.Navigator>
  
);
export default function App() {
  
  const colorScheme = useColorScheme();
  console.log(colorScheme);
  const theme = 
   colorScheme === 'light' 
   ? { ...DTheme, colors: dark.colors}
   : { ...LTheme, colors: light.colors};
  return (
    <SafeAreaProvider>
    <NavigationContainer>
   <PaperProvider theme = {theme}>
   <TabNavigator theme = {theme}/>
    </PaperProvider>
  </NavigationContainer>
  </SafeAreaProvider>
  );
}