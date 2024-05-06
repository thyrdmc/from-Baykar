import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';

export default function MButton(props) {
    const {label} = props
  return (
    <Button variant="contained" className={'mForm'}>
    {label}
    </Button>
  );
}
