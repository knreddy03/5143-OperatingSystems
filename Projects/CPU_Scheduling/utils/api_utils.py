import requests

class APIUtils:
    def __init__(self, config):
        self.base_url = config["base_url"]
        self.client_id = config["client_id"]
        self.config = config

    def init_session(self, seed=None):
        """
        Initializes a session with the API.
        Args:
            seed (int, optional): The seed for reproducibility.
        Returns:
            dict: Contains session_id, start_clock, and time_slice.
        """
        url = f"{self.base_url}/init"
        if seed is not None:
            url += f"?seed={seed}"
        response = requests.post(url, json=self.config)
        if response.status_code == 200:
            return response.json()  # Includes time_slice in the response
        else:
            raise RuntimeError(f"Failed to initialize session: {response.status_code}")

    def get_jobs(self, session_id, clock_time):
        url = f"{self.base_url}/job?client_id={self.client_id}&session_id={session_id}&clock_time={clock_time}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        return []

    def get_burst(self, session_id, job_id):
        url = f"{self.base_url}/burst?client_id={self.client_id}&session_id={session_id}&job_id={job_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        return None

    def bursts_left(self, session_id, job_id):
        url = f"{self.base_url}/burstsLeft?client_id={self.client_id}&session_id={session_id}&job_id={job_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return 0

    def jobs_left(self, session_id):
        url = f"{self.base_url}/jobsLeft?client_id={self.client_id}&session_id={session_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return 0
