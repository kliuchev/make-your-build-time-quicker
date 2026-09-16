import Feature09Domain
import Feature09Data

public enum Feature09PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature09DomainModel = Feature09DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
