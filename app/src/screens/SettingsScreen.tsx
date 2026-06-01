import React, { useState } from 'react';
import { View, Text, StyleSheet, Switch, TouchableOpacity, ScrollView, SafeAreaView, Alert } from 'react-native';
import { translations } from '../localization/translations';

const SettingsScreen = () => {
  const [lang, setLang] = useState<'sw' | 'en'>('sw');
  const [allowUpload, setAllowUpload] = useState(false);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{translations[lang].settings.language}</Text>
          <View style={styles.buttonGroup}>
            <TouchableOpacity
              style={[styles.langButton, lang === 'sw' && styles.activeButton]}
              onPress={() => setLang('sw')}
            >
              <Text style={[styles.langText, lang === 'sw' && styles.activeText]}>Kiswahili</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.langButton, lang === 'en' && styles.activeButton]}
              onPress={() => setLang('en')}
            >
              <Text style={[styles.langText, lang === 'en' && styles.activeText]}>English</Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>{translations[lang].settings.data_privacy}</Text>
          <View style={styles.settingRow}>
            <Text style={styles.settingLabel}>{translations[lang].settings.upload_data}</Text>
            <Switch
              value={allowUpload}
              onValueChange={setAllowUpload}
              trackColor={{ false: '#767577', true: '#2E7D32' }}
              thumbColor={allowUpload ? '#FFF' : '#f4f3f4'}
            />
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Admin / Debug</Text>
          <TouchableOpacity
            style={styles.debugButton}
            onPress={() => Alert.alert('Admin', 'Debugging mode enabled. Image logs will be saved.')}
          >
            <Text style={styles.debugButtonText}>Collect Labeled Images</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.section}>
          <Text style={styles.infoText}>
            App version: 1.0.0
          </Text>
          <Text style={styles.infoText}>
            MosaicAlert © 2026
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  section: {
    backgroundColor: '#FFF',
    padding: 20,
    marginTop: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#EEE',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  buttonGroup: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  langButton: {
    flex: 1,
    padding: 12,
    borderWidth: 1,
    borderColor: '#CCC',
    borderRadius: 8,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  activeButton: {
    backgroundColor: '#2E7D32',
    borderColor: '#2E7D32',
  },
  langText: {
    fontSize: 16,
    color: '#333',
  },
  activeText: {
    color: '#FFF',
    fontWeight: 'bold',
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  settingLabel: {
    fontSize: 16,
    color: '#333',
  },
  debugButton: {
    backgroundColor: '#FFF',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#D32F2F',
    alignItems: 'center',
  },
  debugButtonText: {
    color: '#D32F2F',
    fontWeight: 'bold',
  },
  infoText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginTop: 10,
  },
});

export default SettingsScreen;
