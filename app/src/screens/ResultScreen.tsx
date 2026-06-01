import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, ActivityIndicator, Alert, ScrollView } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import Tts from 'react-native-tts';
import { translations } from '../localization/translations';
import InferenceService from '../ml/InferenceService';
import DatabaseService from '../db/DatabaseService';

const ResultScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { photoPath } = route.params as { photoPath: string };

  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<{ class: string; confidence: number } | null>(null);
  const lang = 'sw';

  useEffect(() => {
    // Initialize TTS
    Tts.getInitStatus().then(() => {
      Tts.setDefaultLanguage(lang === 'sw' ? 'sw-TZ' : 'en-US');
    });

    const runAnalysis = async () => {
      try {
        if (!InferenceService.getIsLoaded()) {
          await InferenceService.initModel();
        }

        const res = await InferenceService.runInference(photoPath);
        setResult(res);

        // Save to Database
        await DatabaseService.saveScan({
          timestamp: new Date().toISOString(),
          prediction: res.class,
          confidence: res.confidence,
          imagePath: photoPath,
          isSynced: 0,
        });
      } catch (e) {
        console.error('Inference/DB error:', e);
        Alert.alert('Error', 'Analysis failed or database error. Please try again.');
        navigation.goBack();
      } finally {
        setLoading(false);
      }
    };

    runAnalysis();

    return () => {
      Tts.stop();
    };
  }, [photoPath, navigation]);

  const speakResult = (text: string) => {
    Tts.stop();
    Tts.speak(text);
  };

  const getResultInfo = () => {
    if (!result) return null;

    const isMosaic = result.class === 'Mosaic';
    const confidence = Math.round(result.confidence * 100);

    if (confidence < 60) {
      return {
        title: translations[lang].result.uncertain,
        actions: translations[lang].result.actions_uncertain,
        color: '#FFA000', // Amber
      };
    } else if (isMosaic) {
      return {
        title: translations[lang].result.mosaic,
        actions: translations[lang].result.actions_mosaic,
        color: '#D32F2F', // Red
      };
    } else {
      return {
        title: translations[lang].result.healthy,
        actions: translations[lang].result.actions_healthy,
        color: '#2E7D32', // Green
      };
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#2E7D32" />
        <Text style={styles.loadingText}>Inachambua picha...</Text>
      </View>
    );
  }

  const resultInfo = getResultInfo();

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.imageContainer}>
        <Image
          source={{ uri: `file://${photoPath}` }}
          style={styles.image}
          resizeMode="cover"
        />
      </View>

      {resultInfo && (
        <View style={[styles.resultCard, { borderColor: resultInfo.color }]}>
          <Text style={[styles.resultTitle, { color: resultInfo.color }]}>
            {resultInfo.title}
          </Text>
          <Text style={styles.confidenceText}>
            {translations[lang].result.confidence}: {Math.round(result!.confidence * 100)}%
          </Text>

          <View style={styles.actionsContainer}>
            <Text style={styles.actionsTitle}>Mapendekezo:</Text>
            <Text style={styles.actionsText}>{resultInfo.actions}</Text>
          </View>

          <TouchableOpacity
            style={styles.speakButton}
            onPress={() => speakResult(`${resultInfo.title}. ${resultInfo.actions}`)}
          >
            <Text style={styles.speakButtonText}>
              {translations[lang].result.listen} (Sikiliza)
            </Text>
          </TouchableOpacity>
        </View>
      )}

      <TouchableOpacity
        style={styles.homeButton}
        onPress={() => navigation.navigate('Home' as never)}
      >
        <Text style={styles.homeButtonText}>Home</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#F5F5F5',
    padding: 20,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 20,
    fontSize: 18,
    color: '#666',
  },
  imageContainer: {
    width: '100%',
    height: 300,
    borderRadius: 12,
    overflow: 'hidden',
    elevation: 3,
    marginBottom: 20,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  resultCard: {
    width: '100%',
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 20,
    borderWidth: 2,
    elevation: 2,
    marginBottom: 20,
  },
  resultTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  confidenceText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  actionsContainer: {
    borderTopWidth: 1,
    borderTopColor: '#EEE',
    paddingTop: 15,
  },
  actionsTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  actionsText: {
    fontSize: 16,
    color: '#444',
    lineHeight: 24,
  },
  speakButton: {
    backgroundColor: '#E8F5E9',
    padding: 12,
    borderRadius: 8,
    marginTop: 20,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#2E7D32',
  },
  speakButtonText: {
    color: '#2E7D32',
    fontSize: 16,
    fontWeight: 'bold',
  },
  homeButton: {
    width: '100%',
    height: 50,
    backgroundColor: '#2E7D32',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
  },
  homeButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default ResultScreen;
