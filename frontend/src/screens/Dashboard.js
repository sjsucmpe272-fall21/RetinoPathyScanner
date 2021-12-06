import React from 'react'
import Background from '../components/Background'
import Logo from '../components/Logo'
import Header from '../components/Header'
import Button from '../components/Button'
import Secondary from '../components/Secondary'
import Supporting from '../components/Supporting'
import { useState, useEffect } from 'react'
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as DocumentPicker from 'expo-document-picker';
import { Image } from 'react-native';
import * as Linking from 'expo-linking';

export default function Dashboard({ navigation }) {
  const [loaded, setLoad] = useState(null);
  const [probability, setProbability] = useState(null);  
  const [jwt_token, setToken] = useState(null);
  const [percentageResult, setResult] = useState(null);
  const [image, setImage] = useState(null);
  const [article, setArticle] = useState(null);

  const openSupportingLink = async () => {
    Linking.openURL('https://www.google.com/search?q=Retinopathy+' + probability);
  }

  const UploadFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({});
    var form = new FormData();
      let token = await AsyncStorage.getItem('jwt_token');
      form.append('image', result.file);
      form.append('token', token);
      fetch(
        'http://ec2-3-145-72-186.us-east-2.compute.amazonaws.com:5000/checkImage', {
          body: form,
          method: "POST"
        }
      ).then((response) => {
        return response.json()
      })
      .then((json)=>{
        console.log(json);
        setProbability(json.result);
        setResult(json.probab);
        setImage(result.uri);
        setLoad(true);

        if(json.result === 'Negligible Possibility') {
          setArticle('Currently you have low chance of retinopathy. Keep it up and click below button to know more.');
        }
        else if(json.result === 'Severe Possibility') {
          setArticle('You have high chances of retinopathy. Kindly click below button to know more.')
        }
        else if(json.result === 'Moderate Possibility') {
          setArticle('It is not too late. Click on below button to know more.');
        }
        else {
          setArticle('Click on below button to know more');
        }

      })
      .catch((error) => {
        console.error(error);
      });
  }

  return (
    <Background>
      <Logo />
      {!loaded && <Header>Upload eye scan below</Header> }
      {!loaded && <Button onPress={UploadFile}> Upload</Button> }
      { loaded && <Button onPress={UploadFile} mode="outlined"> Upload new file</Button> }
      { image && <Image source={{ uri: image }} style={{ width: 300, height: 300 }} />}
      { loaded && <Secondary> { probability }. </Secondary> }
      { loaded && <Secondary> Confidence on result : { Math.round(percentageResult*10000)/100 }%</Secondary> }
      { loaded && <Supporting> {article} </Supporting> }
      { loaded && <Button onPress={openSupportingLink} style={{fontSize: 14}}> Need Help? Click here </Button> }
      <Button
        mode="outlined"
        onPress={() =>{
          AsyncStorage.removeItem('jwt_token')
          navigation.reset({
            index: 0,
            routes: [{ name: 'StartScreen' }],
          })
        }
        }
      >
        Logout
      </Button>
    </Background>
  )
}