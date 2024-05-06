import '../App.css'
import { Box } from '@mui/material'
import MTextField from './forms/mTextField'
import MPasswordField from './forms/MPasswordField'
import MButton from './forms/MButton'
import {Link} from 'react-router-dom'

const Register = () => {
    return(
        <div className={"mBackground"}>
            <Box className={"whiteBoxRegister"}>

                <Box className={"itemBox"}>
                    <Box className={"title"}> User Registration </Box>
                </Box>

                <Box className={"itemBox"}>
                    <MTextField
                        label={"username"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MTextField
                        label={"email"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MPasswordField
                        label={"password"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MPasswordField
                        label={"Confirm password"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MTextField
                        label={"first name"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MTextField
                        label={"last name"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <MButton
                        label={"Register"}
                    />
                </Box>

                <Box className={"itemBox"}>
                    <Link to="/"> Already registred? Please Login </Link>
                </Box>
            </Box>
        </div>
    )
}

export default Register