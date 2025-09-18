# Parody Client - React Native App

A React Native mobile application for receiving and displaying tragedy news alerts.

## Features

- Real-time feed of tragedy news alerts
- Push notifications via Firebase Cloud Messaging
- Pull-to-refresh functionality
- Dark theme UI
- Automatic topic subscription for notifications

## Prerequisites

- Node.js (v16 or higher)
- React Native development environment set up
- iOS: Xcode and CocoaPods
- Android: Android Studio and Android SDK
- Firebase project with Cloud Messaging enabled

## Installation

1. Install dependencies:
```bash
npm install
```

2. iOS setup:
```bash
cd ios && pod install
```

## Firebase Configuration

### iOS Setup

1. Download `GoogleService-Info.plist` from Firebase Console
2. Add it to `ios/parody_client/` in Xcode
3. Ensure it's added to the project target

### Android Setup

1. Download `google-services.json` from Firebase Console
2. Place it in `android/app/`

### Update Backend URL

Edit `App.js` and update the API URL:
```javascript
const API_BASE_URL = 'http://your-backend-url:8000';
```

## Running the App

### iOS
```bash
npm run ios
```

### Android
```bash
npm run android
```

### Metro Bundler
```bash
npm start
```

## App Structure

- `App.js` - Main application component
- `index.js` - App entry point with push notification setup
- `app.json` - React Native configuration
- `package.json` - Dependencies and scripts

## Features Implementation

### Push Notifications

The app automatically:
1. Requests notification permissions on first launch
2. Subscribes to the "tragedies" topic
3. Displays notifications when app is in foreground/background
4. Updates the feed when new notifications arrive

### Feed Display

- Fetches latest 50 articles from backend
- Shows article title and detection timestamp
- Pull-to-refresh to get latest articles
- Dark themed UI for better readability

## Troubleshooting

### iOS Issues

- Ensure you've enabled Push Notifications capability in Xcode
- Check that APNs authentication key is configured in Firebase

### Android Issues

- Make sure `google-services.json` is in the correct location
- Check that Firebase Cloud Messaging is enabled in Firebase Console

### General Issues

- Verify backend is running and accessible
- Check network connectivity
- Review console logs for error messages

## Backend Integration

The app expects the backend to provide:
- `GET /articles` - Returns list of tragedy articles
- Push notifications via Firebase Cloud Messaging to "tragedies" topic

## Development

To customize the app:
1. Modify `App.js` for UI changes
2. Update styles in the StyleSheet
3. Adjust notification handling in `index.js`

## License

MIT