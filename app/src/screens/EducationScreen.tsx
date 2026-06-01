import React from 'react';
import { View, Text, StyleSheet, ScrollView, SafeAreaView, TouchableOpacity } from 'react-native';
import { translations } from '../localization/translations';

const EducationScreen = () => {
  const lang = 'sw';

  const topics = [
    {
      title: translations[lang].education.what_is_mosaic,
      content: 'Ugonjwa wa Mosaic husababishwa na virusi vinavyoenezwa na inzi weupe. Dalili ni pamoja na kubadilika kwa rangi ya majani kuwa ya manjano na kijani kibichi.',
    },
    {
      title: translations[lang].education.how_to_prevent,
      content: 'Ili kuzuia ugonjwa huu, tumia mbegu ambazo zimethibitishwa kuwa safi na kagua shamba lako mara kwa mara.',
    },
    {
      title: translations[lang].education.clean_seeds,
      content: 'Hakikisha mbegu unazopanda zinatoka kwa wauzaji walioidhinishwa au kutoka kwa mimea yenye afya kabisa.',
    },
    {
      title: translations[lang].education.remove_infected,
      content: 'Ukiona mmea wowote wenye dalili, uondoe mara moja na uuchome moto au uuzike ili kuzuia kuenea kwa wadudu.',
    },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.headerTitle}>{translations[lang].education.title}</Text>
        
        {topics.map((topic, index) => (
          <View key={index} style={styles.topicCard}>
            <Text style={styles.topicTitle}>{topic.title}</Text>
            <Text style={styles.topicContent}>{topic.content}</Text>
          </View>
        ))}

        <TouchableOpacity style={styles.moreButton}>
          <Text style={styles.moreButtonText}>{translations[lang].education.learn_more}</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  scrollContent: {
    padding: 20,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 20,
  },
  topicCard: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    elevation: 2,
  },
  topicTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  topicContent: {
    fontSize: 16,
    color: '#666',
    lineHeight: 22,
  },
  moreButton: {
    backgroundColor: '#2E7D32',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  moreButtonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default EducationScreen;
