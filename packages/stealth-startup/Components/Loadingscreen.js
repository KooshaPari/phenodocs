import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Svg, Path } from 'react-native-svg';

export default function Loadingscreen() {
    return (
    		<View style={styles.Loadingscreen}>
      			<View style={styles.rectangle7}/>
      			{/* component basicCircle */}
      			<View style={styles.basicCircle}>
<Svg style={styles.icon} width="23" height="21" viewBox="0 0 23 21" fill="none" >
<Path fillRule="evenodd" clipRule="evenodd" d="M0.958313 10.5C0.958313 15.8157 5.67798 20.125 11.5 20.125C17.322 20.125 22.0416 15.8157 22.0416 10.5C22.0416 5.18426 17.322 0.875 11.5 0.875C5.67798 0.875 0.958313 5.18426 0.958313 10.5ZM20.125 10.5C20.125 14.8492 16.2634 18.375 11.5 18.375C6.73652 18.375 2.87498 14.8492 2.87498 10.5C2.87498 6.15076 6.73652 2.625 11.5 2.625C16.2634 2.625 20.125 6.15076 20.125 10.5Z" fill="black"/>
</Svg>

      			</View>
      			{/* Vigma RN:: can be replaced with <_basicCircle  /> */}
      			<View style={styles._basicCircle}>
<Svg style={styles._icon} width="22" height="21" viewBox="0 0 22 21" fill="none" >
<Path fillRule="evenodd" clipRule="evenodd" d="M0.916687 10.5C0.916687 15.8157 5.43115 20.125 11 20.125C16.5689 20.125 21.0834 15.8157 21.0834 10.5C21.0834 5.18426 16.5689 0.875 11 0.875C5.43115 0.875 0.916687 5.18426 0.916687 10.5ZM19.25 10.5C19.25 14.8492 15.5564 18.375 11 18.375C6.44367 18.375 2.75002 14.8492 2.75002 10.5C2.75002 6.15076 6.44367 2.625 11 2.625C15.5564 2.625 19.25 6.15076 19.25 10.5Z" fill="black"/>
</Svg>

      			</View>
      			{/* Vigma RN:: can be replaced with <__basicCircle  /> */}
      			<View style={styles.__basicCircle}>
<Svg style={styles.__icon} width="23" height="21" viewBox="0 0 23 21" fill="none" >
<Path fillRule="evenodd" clipRule="evenodd" d="M0.958313 10.5C0.958313 15.8157 5.67798 20.125 11.5 20.125C17.322 20.125 22.0416 15.8157 22.0416 10.5C22.0416 5.18426 17.322 0.875 11.5 0.875C5.67798 0.875 0.958313 5.18426 0.958313 10.5ZM20.125 10.5C20.125 14.8492 16.2634 18.375 11.5 18.375C6.73652 18.375 2.87498 14.8492 2.87498 10.5C2.87498 6.15076 6.73652 2.625 11.5 2.625C16.2634 2.625 20.125 6.15076 20.125 10.5Z" fill="black"/>
</Svg>

      			</View>
      			{/* Vigma RN:: can be replaced with <___basicCircle  /> */}
      			<View style={styles.___basicCircle}>
<Svg style={styles.___icon} width="22" height="21" viewBox="0 0 22 21" fill="none" >
<Path fillRule="evenodd" clipRule="evenodd" d="M0.916687 10.5C0.916687 15.8157 5.43115 20.125 11 20.125C16.5689 20.125 21.0834 15.8157 21.0834 10.5C21.0834 5.18426 16.5689 0.875 11 0.875C5.43115 0.875 0.916687 5.18426 0.916687 10.5ZM19.25 10.5C19.25 14.8492 15.5564 18.375 11 18.375C6.44367 18.375 2.75002 14.8492 2.75002 10.5C2.75002 6.15076 6.44367 2.625 11 2.625C15.5564 2.625 19.25 6.15076 19.25 10.5Z" fill="black"/>
</Svg>

      			</View>
      			{/* Vigma RN:: can be replaced with <____basicCircle  /> */}
      			<View style={styles.____basicCircle}>
<Svg style={styles.____icon} width="22" height="21" viewBox="0 0 22 21" fill="none" >
<Path fillRule="evenodd" clipRule="evenodd" d="M0.916687 10.5C0.916687 15.8157 5.43115 20.125 11 20.125C16.5689 20.125 21.0834 15.8157 21.0834 10.5C21.0834 5.18426 16.5689 0.875 11 0.875C5.43115 0.875 0.916687 5.18426 0.916687 10.5ZM19.25 10.5C19.25 14.8492 15.5564 18.375 11 18.375C6.44367 18.375 2.75002 14.8492 2.75002 10.5C2.75002 6.15076 6.44367 2.625 11 2.625C15.5564 2.625 19.25 6.15076 19.25 10.5Z" fill="black"/>
</Svg>

      			</View>
      			<Text style={styles.imagesofithere}>
        				{`Images of it here`}
      			</Text>
      			<Text style={styles.secondPageSkip}>
        				{`Second Page (Skip) `}
      			</Text>
      			<Text style={styles.ourSloganFeacturesweoffer}>
        				{`Our Slogan/Feactures we offer`}
      			</Text>
      			<View style={styles.rectangle9}/>
      			<Text style={styles.createAnAccount}>
        				{`Create An Account`}
      			</Text>
      			<View style={styles.rectangle15}/>
      			<Text style={styles.signIn}>
        				{`Sign In`}
      			</Text>
    		</View>
    )
}

const styles = StyleSheet.create({
  	Loadingscreen: {
    flexShrink: 0,
    height: 566,
    width: 299,
    backgroundColor: "rgba(255, 255, 255, 1)",
    alignItems: "flex-start",
    rowGap: 0
},
  	rectangle7: {
    position: "absolute",
    flexShrink: 0,
    width: 299,
    height: 566,
    backgroundColor: "rgba(95, 152, 125, 0.6)"
},
  	basicCircle: {
    position: "absolute",
    flexShrink: 0,
    top: 276,
    bottom: 269,
    left: 55,
    right: 221,
    alignItems: "flex-start",
    rowGap: 0
},
  	icon: {
    position: "absolute",
    flexShrink: 0,
    top: 1,
    left: 1,
    width: 21,
    height: 19,
    overflow: "visible"
},
  	_basicCircle: {
    position: "absolute",
    flexShrink: 0,
    top: 276,
    bottom: 269,
    left: 98,
    right: 179,
    alignItems: "flex-start",
    rowGap: 0
},
  	_icon: {
    position: "absolute",
    flexShrink: 0,
    top: 1,
    left: 1,
    width: 20,
    height: 19,
    overflow: "visible"
},
  	__basicCircle: {
    position: "absolute",
    flexShrink: 0,
    top: 276,
    bottom: 269,
    left: 140,
    right: 136,
    alignItems: "flex-start",
    rowGap: 0
},
  	__icon: {
    position: "absolute",
    flexShrink: 0,
    top: 1,
    left: 1,
    width: 21,
    height: 19,
    overflow: "visible"
},
  	___basicCircle: {
    position: "absolute",
    flexShrink: 0,
    top: 276,
    bottom: 269,
    left: 183,
    right: 94,
    alignItems: "flex-start",
    rowGap: 0
},
  	___icon: {
    position: "absolute",
    flexShrink: 0,
    top: 1,
    left: 1,
    width: 20,
    height: 19,
    overflow: "visible"
},
  	____basicCircle: {
    position: "absolute",
    flexShrink: 0,
    top: 276,
    bottom: 269,
    left: 225,
    right: 52,
    alignItems: "flex-start",
    rowGap: 0
},
  	____icon: {
    position: "absolute",
    flexShrink: 0,
    top: 1,
    left: 1,
    width: 20,
    height: 19,
    overflow: "visible"
},
  	imagesofithere: {
    position: "absolute",
    flexShrink: 0,
    top: 154,
    left: 66,
    width: 165,
    height: 40,
    textAlign: "left",
    color: "rgba(0, 0, 0, 1)",
    fontFamily: "Inter",
    fontSize: 20,
    fontWeight: "400",
    letterSpacing: 0
},
  	secondPageSkip: {
    position: "absolute",
    flexShrink: 0,
    top: 13,
    left: 21,
    width: 263,
    height: 24,
    textAlign: "center",
    color: "rgba(0, 0, 0, 1)",
    fontFamily: "Inter",
    fontSize: 20,
    fontWeight: "400",
    letterSpacing: 0
},
  	ourSloganFeacturesweoffer: {
    position: "absolute",
    flexShrink: 0,
    top: 317,
    left: 68,
    width: 190,
    height: 21,
    textAlign: "left",
    color: "rgba(0, 0, 0, 1)",
    fontFamily: "Inter",
    fontSize: 12,
    fontWeight: "400",
    letterSpacing: 0
},
  	rectangle9: {
    position: "absolute",
    flexShrink: 0,
    top: 439,
    left: 55,
    width: 190,
    height: 31,
    backgroundColor: "rgba(217, 217, 217, 1)"
},
  	createAnAccount: {
    position: "absolute",
    flexShrink: 0,
    top: 439,
    right: 54,
    left: 55,
    height: 22,
    textAlign: "center",
    color: "rgba(0, 0, 0, 1)",
    fontFamily: "Inter",
    fontSize: 20,
    fontWeight: "700",
    letterSpacing: 0
},
  	rectangle15: {
    position: "absolute",
    flexShrink: 0,
    top: 391,
    left: 55,
    width: 190,
    height: 31,
    backgroundColor: "rgba(72, 203, 51, 1)"
},
  	signIn: {
    position: "absolute",
    flexShrink: 0,
    top: 395,
    right: 55,
    left: 55,
    height: 22,
    textAlign: "center",
    color: "rgba(0, 0, 0, 1)",
    fontFamily: "Inter",
    fontSize: 20,
    fontWeight: "700",
    letterSpacing: 0
}
})
