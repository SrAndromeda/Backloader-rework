import axios from "axios";
import { BASE_BACKEND, BASE_FLOW, BASE_OUTLET } from "app/utils/constant";

export const fetchFlow = async (setContent) => {
    axios.get(BASE_BACKEND + BASE_FLOW)
        .then((response) => {
            setContent(response.data)
            // console.log(response.data)
        })
        .catch((error) => {
            console.error(error)
        })
};

export const fetchOutlet = async (setContent) => {
    axios.get(BASE_BACKEND + BASE_OUTLET)
        .then((response) => {
            setContent(response.data)
            // console.log(response.data)
        })
        .catch((error) => {
            console.error(error)
        })
};