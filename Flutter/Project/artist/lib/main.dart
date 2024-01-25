import 'package:flutter/material.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('앱 타이틀'),
          actions: <Widget>[
            IconButton(
              icon: Icon(Icons.search),
              onPressed: () {
                // 검색 기능 구현
              },
            ),
          ],
        ),
        body: ListView(
          children: <Widget>[
            Container(
              height: 200,
              color: Colors.grey, // 배너 자리
              child: Center(child: Text('banner')),
            ),
            // 여기에 다른 콘텐츠 영역을 구현
          ],
        ),
        bottomNavigationBar: BottomNavigationBar(
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.shuffle),
              label: 'Random',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.notifications),
              label: 'Notifications',
            ),
          ],
          // 여기에 탭 기능을 추가할 수 있음
        ),
      ),
    );
  }
}
