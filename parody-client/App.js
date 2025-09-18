import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  FlatList,
  RefreshControl,
  Alert,
  Platform,
  ActivityIndicator,
} from 'react-native';
import messaging from '@react-native-firebase/messaging';
import PushNotification from 'react-native-push-notification';

const API_BASE_URL = 'http://localhost:8000'; // Update with your backend URL

const App = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // Initialize push notifications
  useEffect(() => {
    initializePushNotifications();
    requestUserPermission();
    subscribeToPushTopic();
    setupNotificationListeners();
    fetchArticles();
  }, []);

  const initializePushNotifications = () => {
    if (Platform.OS === 'android') {
      PushNotification.createChannel(
        {
          channelId: 'tragedy-alerts',
          channelName: 'Tragedy Alerts',
          channelDescription: 'Notifications for tragedy news',
          importance: 4,
          vibrate: true,
        },
        (created) => console.log(`Channel created: ${created}`)
      );
    }
  };

  const requestUserPermission = async () => {
    const authStatus = await messaging().requestPermission();
    const enabled =
      authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
      authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
      console.log('Authorization status:', authStatus);
      const token = await messaging().getToken();
      console.log('FCM Token:', token);
      // Send token to your backend if needed
    }
  };

  const subscribeToPushTopic = async () => {
    try {
      await messaging().subscribeToTopic('tragedies');
      console.log('Subscribed to tragedies topic');
    } catch (error) {
      console.error('Error subscribing to topic:', error);
    }
  };

  const setupNotificationListeners = () => {
    // Handle notifications when app is in foreground
    const unsubscribe = messaging().onMessage(async (remoteMessage) => {
      console.log('Foreground notification:', remoteMessage);
      
      // Show local notification
      PushNotification.localNotification({
        channelId: 'tragedy-alerts',
        title: remoteMessage.notification?.title || 'Tragedy Alert',
        message: remoteMessage.notification?.body || 'New tragedy detected',
        data: remoteMessage.data,
      });

      // Add to feed
      if (remoteMessage.data) {
        const newArticle = {
          id: Date.now().toString(),
          title: remoteMessage.notification?.body?.replace(/" — Don't forget to read it!/g, '') || 'Unknown',
          url: remoteMessage.data.url,
          detected_at: new Date().toISOString(),
        };
        setArticles(prev => [newArticle, ...prev]);
      }
    });

    // Handle background notifications
    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('Background notification:', remoteMessage);
      // Notification will be shown automatically
    });

    // Handle notification tap
    messaging().onNotificationOpenedApp((remoteMessage) => {
      console.log('Notification opened app:', remoteMessage);
      // Handle navigation to article if needed
    });

    return unsubscribe;
  };

  const fetchArticles = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/articles?limit=50`);
      const data = await response.json();
      setArticles(data.articles || []);
    } catch (error) {
      console.error('Error fetching articles:', error);
      Alert.alert('Error', 'Failed to fetch articles');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchArticles();
  };

  const renderArticle = ({ item }) => (
    <View style={styles.articleCard}>
      <Text style={styles.articleTitle} numberOfLines={2}>
        {item.title}
      </Text>
      <Text style={styles.articleTime}>
        {new Date(item.detected_at).toLocaleString()}
      </Text>
    </View>
  );

  const ListEmptyComponent = () => (
    <View style={styles.emptyContainer}>
      <Text style={styles.emptyText}>No tragedy alerts yet</Text>
      <Text style={styles.emptySubtext}>Pull down to refresh</Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Tragedy Alerts</Text>
        <Text style={styles.headerSubtitle}>Real-time news monitoring</Text>
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#FF6B6B" />
        </View>
      ) : (
        <FlatList
          data={articles}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderArticle}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={['#FF6B6B']}
              tintColor="#FF6B6B"
            />
          }
          ListEmptyComponent={ListEmptyComponent}
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1A1A1A',
  },
  header: {
    backgroundColor: '#2A2A2A',
    paddingVertical: 20,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF6B6B',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#999',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContent: {
    paddingVertical: 8,
  },
  articleCard: {
    backgroundColor: '#2A2A2A',
    marginHorizontal: 16,
    marginVertical: 6,
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#FF6B6B',
  },
  articleTitle: {
    fontSize: 16,
    color: '#FFFFFF',
    marginBottom: 8,
    lineHeight: 22,
  },
  articleTime: {
    fontSize: 12,
    color: '#777',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 100,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#555',
  },
});

export default App;