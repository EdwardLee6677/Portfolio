import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Artist Portfolio'),
          backgroundColor: Colors.green,
        ),
        body: Column(
          children: [
            Container(
              width: 200, 
              height: 200, 
              color: Colors.green,
              margin: EdgeInsets.all(00),
            ),
            Container(
              width: 200, 
              height: 200, 
              color: Colors.yellow,
              margin: EdgeInsets.all(20),
            ),
            Container(
              width: 200, 
              height: 200, 
              color: Colors.red,
              padding: EdgeInsets.all(20),
              child: Text('Hello World!'),
            ),
            Container(
              width: 200, 
              height: 200, 
              color: Colors.blue,
              padding: EdgeInsets.fromLTRB(10, 40, 20, 20),
              child: Text('Hello World!'),
            ),
          ],
        )  
      )
    );
  }
}