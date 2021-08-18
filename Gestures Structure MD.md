# How to Access Gesture Data



## Structure

```markdown
public struct GestureData{
        //statuses
        //Shuriken
        public bool throw_shuriken;
        public bool is_r_shuriken;
        public bool is_l_shuriken;
        //Push/Pointer
        public bool is_hand_push;
        public bool is_r_hand_push;
        public bool is_l_hand_push;

        //Lights/Swing
        public bool is_hand_lights;
        public bool is_r_hand_lights;
        public bool is_l_hand_lights;

        //Clap
        public bool is_hand_clap;

        //throw seed
        public bool is_throw_seed;
        public bool is_r_throw_seed;
        public bool is_l_throw_seed;

        //direction values
        //Shuriken
        public float r_shuriken_x;
        public float r_shuriken_y;
        public float r_shuriken_z;
        public float l_shuriken_x;
        public float l_shuriken_y;
        public float l_shuriken_z;
        //Push/Pointer
        public float r_push_x;
        public float r_push_y;
        public float r_push_z;
        public float l_push_x;
        public float l_push_y;
        public float l_push_z;
    }
```



### Access Point

```markdown
GameObject DataHold = GameObject.Find("GestureData");
ConnectedSeatApiGesture AccessData = DataHold.GetComponent<ConnectedSeatApiGesture>();
```

Exposed variables: (Read)

```
AccessData.OutputGesture.throw_shuriken
```