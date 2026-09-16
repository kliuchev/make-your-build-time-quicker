import Feature04Domain
import Feature04Data

public enum Feature04PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature04DomainModel = Feature04DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
