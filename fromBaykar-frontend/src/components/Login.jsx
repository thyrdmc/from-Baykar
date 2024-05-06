import '../App.css'
import { Box } from '@mui/material'
import MTextField from './forms/mTextField'
import MPasswordField from './forms/MPasswordField'
import MButton from './forms/MButton'
import {Link} from 'react-router-dom'

const Login = () => {
    return(
        <div className={"mBackground"}>
            <Box className={"whiteBox"}>

                <Box className={"itemBox"}>
                    <Box className={"title"}> Login for Auth App </Box>
                </Box>

                <Box className={"itemBox"}>
                    <MTextField
                        label={"username"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MPasswordField
                        label={"password"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MButton
                        label={"login"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <Link to="/register"> Sign Up </Link>
                </Box>
            </Box>
        </div>
    )
}

export default Login