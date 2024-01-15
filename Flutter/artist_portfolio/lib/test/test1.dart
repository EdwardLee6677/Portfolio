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
            Text('Hello World!'),
            Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.star, size: 48, color: Colors.green),
            Icon(Icons.star, size: 48, color: Colors.green),
            Icon(Icons.star, size: 48, color: Colors.green),
          ]
          ),
          ],  
        ),
        bottomNavigationBar: BottomAppBar(
          child: SizedBox(
            height: 100,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Icon(Icons.phone, size: 48, color: Colors.black),
                Icon(Icons.message, size: 48, color: Colors.black),
                Icon(Icons.contact_page, size: 48, color: Colors.black),
              ],),
          )
        )
        )
      );
  }
}