import Feature14Domain
import Feature14Data

public enum Feature14PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature14DomainModel = Feature14DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
