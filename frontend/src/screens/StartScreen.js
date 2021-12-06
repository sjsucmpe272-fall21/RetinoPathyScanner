import React, { useEffect, useState } from 'react'
import Background from '../components/Background'
import Logo from '../components/Logo'
import Header from '../components/Header'
import Button from '../components/Button'
import Paragraph from '../components/Paragraph'
import AsyncStorage from '@react-native-async-storage/async-storage';


export default function StartScreen({ navigation }) {
  
  useEffect(()=> {
  AsyncStorage.getItem('jwt_token').then((token)=>{
    console.log(token !== "null")
    if(token && token !== null && token !== "")
    {
      console.log("I was here")
      navigation.navigate('Dashboard')
    }
  })
  .catch((err)=>{

  })
})

  return (
    <Background>
      <Logo />
      <Header>Retinopathy Scanner</Header>
      <Paragraph>
        Detect Retinopathy by uploading eye scans.
      </Paragraph>
      
        <Button
          mode="contained"
          onPress={() => navigation.navigate('LoginScreen')}
        >
          Login
        </Button>
        <Button
          mode="outlined"
          onPress={() => navigation.navigate('RegisterScreen')}
        >
          Sign Up
        </Button>
      
      
    </Background>
  )
}
