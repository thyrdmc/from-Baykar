import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

export default function MTextField(props) {
    const {label} = props
  return (
      <TextField 
                id="outlined-basic" 
                label={label}
                variant="outlined" 
                className={"mForm"}
        />
  );
}
