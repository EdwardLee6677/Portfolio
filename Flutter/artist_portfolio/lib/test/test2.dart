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
              margin: EdgeInsets.fromLTRB(0,0,40,0),
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
            Align(
              alignment: Alignment.topRight,
              child: Container(
                width: double.infinity, 
                height: 200,
                decoration: 
                  BoxDecoration(
                    color: const Color.fromARGB(114, 33, 149, 243),
                    border: Border.all(
                      color: Colors.black,
                      width: 5,
                    ),
                    borderRadius: BorderRadius.circular(20),
                  ),
              ),
            ),
          ],
        )  
      )
    );
  }
}