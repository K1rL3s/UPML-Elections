import { isVoteDisplayShown } from "src/store/MainStore/getters";

export function login(state, sessionId) {
  state.sessionId = sessionId;
}

export function mutateVote(state) {
  state.isVoted = true;
}

export function toggleVoteDisplay(state) {
  state.isVoteDisplayShown = !state.isVoteDisplayShown;
}
export function toggleNameShow(state) {
  state.isNameShown = !state.isNameShown;
}
export function changeCandidatesShown(state, arr) {
  state.candidatesShow = arr;
}
export function changeRole(state, role) {
  state.role = role;
}

export function toggleEnd(state) {
  state.isEnded = !state.isEnded;
}
export function changeWinnerName(state, name) {
  state.winnerName = name;
}
